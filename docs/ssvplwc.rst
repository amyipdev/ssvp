SSVPLWC
=======

SSVPLWC is a very simple protocol for creating custom detectors. While the protocol
can be implemented in any language, the default template exists in Rust.

There is no packaging of SSVPLWC, because it's designed to be self-modified.
If you want to use the default implementation, leave the files as is, and on the
target server, run:

.. code-block:: bash

    make ssvlpwc
    
That method is also how you can generally run SSVPLWC.

Extending the Rust Template
---------------------------

The basic implementation of SSVPLWC is located at :code:`srv/ssvplwc`. This
is a Cargo-based Rust project, and the main source file is located at
:code:`srv/ssvplwc/src/main.rs`.

By default, SSVPLWC will run on TCP port :code:`29831`. To change this, find
the line in :code:`main` which defines the variable :code:`lsn`, and change
the port number, for instance:

.. code-block:: rust
    
    // old listener:
    // let lsn = TcpListener::bind("[::]:29831")?;
    // new listener:
    let lsn = TcpListener::bind("[::]:5555")?;

By default, SSVPLWC will simply write back :code:`ssvp-ok`, which indicates
that the server works. This is effectively equivalent to using the :code:`tcp`
module to ping a netcat listener, or some other always-on TCP listener, with
the added caveat that `ssvp-ok` must be returned (indicating return data
transfer is possible).

The recommendation is to build a test-case function, for instance:

.. code-block:: rust

    fn test_server() -> bool {
        1 + 1 == 2
    }    

You should then change the lines which return the result to be conditional:

.. code-block:: rust

    let mut st = st.unwrap();
    // st.write(b"ssvp-ok")?;
    if test_server() {
        st.write(b"ssvp-ok")?;
    } else {
        st.write(b"ssvp-error")?;
    }    

Protocol Details
----------------

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in `RFC 2119 <https://datatracker.ietf.org/doc/html/rfc2119>`_.

The key word "UNLESS" provides a specific-circumstances exception to the words
"MUST", "MUST NOT", or "REQUIRED".

The key word "bytestring" means a string of bytes representing UTF-8-encoded ASCII characters
which can legally be transmitted using the TCP/IP protocol stack.

Define two servers, :code:`A` and :code:`B`, which implement the SSVPLWC protocol.
:code:`A` is fetching information (the client), and :code:`B` is returning information (the server).

Define a TCP/IP port, :code:`port`, which can be set as any valid TCP/IP port number
(an integer from 1 to 65535), and which is presumed by default to be :code:`29831`.

Define the yielded value of a transaction under the SSVPLWC protocol to be one of the following states:

- **Operational**: The server is not having any major disruptive problems.
- **Critical Failure**: The server is having a major disruptive problem.

Making a Transaction
~~~~~~~~~~~~~~~~~~~~

:code:`A` initiates a TCP connection on :code:`port` to :code:`B`. Both servers should behave
properly according to the TCP specification (`RFC 793 <https://www.ietf.org/rfc/rfc793.txt>`_).
This TCP connection should be made over either IPv4 (`RFC 791 <https://datatracker.ietf.org/doc/html/rfc791>`_)
or IPv6 (`RFC 2460 <https://datatracker.ietf.org/doc/html/rfc2460>`_). :code:`A` and :code:`B`
do not have to support the same IP version, or use the same IP version, as long as a translation
layer between the two versions is implemented correctly.

Once the connection between the two servers has been made, :code:`B` should begin running
user-defined tests to determine whether to present it as properly functioning. These tests
MUST result in a boolean value.

- If the value is a truth value, then :code:`B` MUST send a packet consisting of the byte-string
  :code:`ssvp-ok`, with no other characters, whitespace, or padding. :code:`A` MUST interpret this
  result as an Operational.
- If the value is a falseness value, then :code:`B` must send a packet. The contents of the packet
  MAY be used by :code:`A` to present different states; however, the packet MUST indicate an error.
  If the different states are not supported by :code:`A`, :code:`A` MUST interpret the result
  as a Critical Failure. SSVPLWC MUST NOT be used for communicating whether other alternative states
  are supported by two implementers of the SSVPLWC protocol; however, two servers MAY use another
  protocol or means of communication to determine what codes are supported, and MAY use another
  protocol to switch the results yielded by :code:`B` upon failure in accordance with pre-negotiated
  codes.

In the event of a falseness value, the default returned bytestring SHOULD be :code:`ssvp-error`.
However, :code:`A` MUST support the return value being any valid bytestring, and MUST NOT
treat :code:`ssvp-error` differently from other non-:code:`ssvp-ok` bytestrings UNLESS alternative
handlings have been prenegotiated through an external protocol.

Failure to Connect
~~~~~~~~~~~~~~~~~~

If while attempting to establish the TCP connection, or at any point during the connection, the
connection fails, :code:`A` MUST yield a Critical Failure for that test.