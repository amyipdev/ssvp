for filename in *.ts; do
    echo ${filename%.ts}.js
done