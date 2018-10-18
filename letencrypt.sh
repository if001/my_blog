#!/bin/sh

#証明書のドメイン（,区切りで複数のドメインも指定可能）
DOMAIN=www.if-blog.site

#ドキュメントルート（上のドメインで接続可能である必要がある）
WEBROOT=/var/www/letsencrypt
if [ ! -e ${WEBROOT} ]; then
    sudo mkdir -p /var/www/letsencrypt
fi

#メールアドレス（トラブル時にメールが届く）
EMAIL=otomijuf.002@gmail.com

sudo certbot certonly -m $EMAIL --agree-tos --non-interactive $* --webroot -w $WEBROOT -d $DOMAIN

mv /etc/letsencrypt/live/${DOMAIN}/fullchain.pem nginx/key/fullchain.pem
mv /etc/letsencrypt/live/${DOMAIN}/chain.pem     nginx/key/chain.pem 
mv /etc/letsencrypt/live/example.com/privkey.pem nginx/key/privkey.pem 


