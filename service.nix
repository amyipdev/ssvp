{ pkgs, config, lib, ... }:

with lib;

let 
	python3 = pkgs.python311.withPackages (ps: with ps; [
        flask
        mysql-connector
        ping3
		requests
        psycopg2
		gunicorn
	]);
	
	cfg = config.services.ssvp;
	npmlock2nix = import (builtins.fetchTarball
		"https://github.com/nix-community/npmlock2nix/archive/9197bbf.tar.gz"
	) {};
	nodeModules = npmlock2nix.v2.node_modules {
		src = ./.;
		installPhase = "mv node_modules $out/";
	};
	ins = pkgs.runCommand "ssvp" {src = ./.; buildInputs = with pkgs; [ nodejs ];} ''
		cp -r --no-preserve=all $src $out
		cd $out 
		cp -r ${nodeModules} node_modules
		make 
	'';

in {
   	options.services.ssvp = {
		enable = mkEnableOption "SSVP Production Environment";
		configFile = mkOption {
			type = types.str;
			description = "Configuration file";
		};
	};
	config = mkIf cfg.enable {
    		systemd.services.ssvp-gunicorn = {
        		path = with pkgs; [
            			python3
            			which
            			jq
            			bash
        		];
			wantedBy = [ "multi-user.target" ];
			after = [ "network.target" ];
        		script = ''
				cd ${ins}
				${pkgs.bash}/bin/bash srv/gunicorn.sh
        		'';
			environment = { SSVP_CONFIG = cfg.configFile; };
    		};
		systemd.timers.ssvp-interval = {
			wantedBy = [ "timers.target" ];
			timerConfig = {
				OnUnitActiveSec = "5m";
				Unit = "ssvp-interval.service";
			};
		};
		systemd.services.ssvp-interval = {	
        		path = with pkgs; [
            			python3
            			bash
        		];
			wantedBy = [ "multi-user.target" ];
			after = [ "network.target" ];
			script = ''
				cd ${ins}
				${python3}/bin/python3 srv/interval.py
			'';
			serviceConfig = {
				Type = "oneshot";
			};
			environment = { SSVP_CONFIG = cfg.configFile; };
		};
	};
}
