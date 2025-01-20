openssl req -newkey rsa:4096 \
            -x509 \
            -sha256 \
            -days 10950 \
            -nodes \
            -out old.crt \
            -keyout old.key \
            -addext "subjectAltName = DNS:(OLDDOMAIN)" \
            -subj /C=US/ST=USA

openssl req -newkey rsa:4096 \
            -x509 \
            -sha256 \
            -days 10950 \
            -nodes \
            -out new.crt \
            -keyout new.key \
            -addext "subjectAltName = DNS:(NEWDOMAIN)" \
            -subj /C=US/ST=USA

openssl req -newkey rsa:4096 \
            -x509 \
            -sha256 \
            -days 10950 \
            -nodes \
            -out dummy.crt \
            -keyout dummy.key \
            -addext "subjectAltName = DNS:dummy.com" \
            -subj /C=US/ST=USA
