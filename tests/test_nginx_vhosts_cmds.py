import unittest
from src.vhosts_commands.nginx_vhosts_cmds import NginxVhostsCmds


class TestNginxVhostsCmds(unittest.TestCase):
    def setUp(self):
        self.cmds = NginxVhostsCmds()

    def test_basic_vhosts_extraction(self):
        content = """
        server {
            listen 80;
            server_name example.com www.example.com;
        }
        server {
            listen 443 ssl;
            server_name secure.example.com;
        }
        """
        expected_vhosts = {'example.com', 'www.example.com', 'secure.example.com'}
        result_vhosts = self.cmds.get_all_vhosts_from_content(content)
        self.assertSetEqual(expected_vhosts, result_vhosts)

    def test_with_comments_and_whitespace(self):
        content = """
        # This is a comment line
        server {
            listen 80;
            server_name example.org www.example.org;  # Another comment
        }

        # Another server block
        server {
            listen 443 ssl;
            server_name secure.example.org;
            # End of block
        }
        """
        expected_vhosts = {'example.org', 'www.example.org', 'secure.example.org'}
        result_vhosts = self.cmds.get_all_vhosts_from_content(content)
        self.assertSetEqual(expected_vhosts, result_vhosts)

    def test_with_comments_in_the_middle(self):
        content = """
        # This is a comment line
        server {
            listen 80;
            server_name example.org; # www.example.org;
        }

        # Another server block
        server {
            listen 443 ssl;
            server_name secure.example.org;
            # End of block
        }
        """
        expected_vhosts = {'example.org', 'secure.example.org'}
        result_vhosts = self.cmds.get_all_vhosts_from_content(content)
        self.assertSetEqual(expected_vhosts, result_vhosts)

    def test_with_variables_and_no_server_name(self):
        content = """
        server {
            listen 80;
            server_name $hostname;
        }
        server {
            listen 80;
            root /var/www/html;
        }
        """
        # Expecting an empty set since one server_name uses a variable and the other block has no server_name
        expected_vhosts = set()
        result_vhosts = self.cmds.get_all_vhosts_from_content(content)
        self.assertSetEqual(expected_vhosts, result_vhosts)

    def test_duplicate_server_names(self):
        content = """
        server {
            listen 80;
            server_name example.net www.example.net;
        }
        server {
            listen 80;
            server_name www.example.net example.net;
        }
        """
        # Expecting unique server names, despite being listed more than once
        expected_vhosts = {'example.net', 'www.example.net'}
        result_vhosts = self.cmds.get_all_vhosts_from_content(content)
        self.assertSetEqual(expected_vhosts, result_vhosts)

    def test_empty_content(self):
        content = ""
        # Expecting an empty set since there's no content
        expected_vhosts = set()
        result_vhosts = self.cmds.get_all_vhosts_from_content(content)
        self.assertSetEqual(expected_vhosts, result_vhosts)

    def test_wildcarts(self):
        content = """
        server {
          # Replace this port with the right one for your requirements
          listen 80 default_server;  #could also be 1.2.3.4:80
        
          # Multiple hostnames separated by spaces.  Replace these as well.
          server_name star.yourdomain.com *.yourdomain.com; # Alternately: _
        
          root /PATH/TO/WEBROOT;
        
          error_page 404 errors/404.html;
          access_log logs/star.yourdomain.com.access.log;
        
          index index.php index.html index.htm;
        
          # static file 404's aren't logged and expires header is set to maximum age
          location ~* \.(jpg|jpeg|gif|css|png|js|ico|html)$ {
            access_log off;
            expires max;
          }
        
          location ~ \.php$ {
            include fastcgi_params;
            fastcgi_intercept_errors on;
            # By all means use a different server for the fcgi processes if you need to
            fastcgi_pass   127.0.0.1:YOURFCGIPORTHERE;
          }
        
          location ~ /\.ht {
            deny  all;
          }
        }
        """
        expected_vhosts = {'star.yourdomain.com', '*.yourdomain.com'}
        result_vhosts = self.cmds.get_all_vhosts_from_content(content)
        self.assertSetEqual(expected_vhosts, result_vhosts)

    def test_include_server_name_settings1(self):
        content = """
        http {
          index index.html;

          server {
            server_name www.domain1.com;
            access_log logs/domain1.access.log main;
            
            server_name_in_redirect on;
            server_tokens on;
            root /var/www/domain1.com/htdocs;
          }

          server {
            server_name_in_redirect off;
            server_name www.domain2.com;
            access_log  logs/domain2.access.log main;

            root /var/www/domain2.com/htdocs;
          }
        }
        """
        expected_vhosts = {'www.domain1.com', 'www.domain2.com'}
        result_vhosts = self.cmds.get_all_vhosts_from_content(content)
        self.assertSetEqual(expected_vhosts, result_vhosts)

    def test_include_server_name_settings2(self):
        content = """
        http {
          index index.html;
          server_names_hash_bucket_size 32|64|128;    
        
          server {
            server_name www.domain1.com;
            access_log logs/domain1.access.log main;

            server_name_in_redirect on;
            server_tokens on;
            root /var/www/domain1.com/htdocs;
          }

          server {
            server_name www.domain2.com;
            access_log  logs/domain2.access.log main;

            root /var/www/domain2.com/htdocs;
          }
        }
        """
        expected_vhosts = {'www.domain1.com', 'www.domain2.com'}
        result_vhosts = self.cmds.get_all_vhosts_from_content(content)
        self.assertSetEqual(expected_vhosts, result_vhosts)

    def test_include_server_name_settings3(self):
        content = """
        http {
          index index.html;
          server_names_hash_max_size 512;    

          server {
            server_name www.domain1.com;
            access_log logs/domain1.access.log main;

            server_name_in_redirect on;
            server_tokens on;
            root /var/www/domain1.com/htdocs;
          }

          server {
            server_name www.domain2.com;
            access_log  logs/domain2.access.log main;

            root /var/www/domain2.com/htdocs;
          }
        }
        """
        expected_vhosts = {'www.domain1.com', 'www.domain2.com'}
        result_vhosts = self.cmds.get_all_vhosts_from_content(content)
        self.assertSetEqual(expected_vhosts, result_vhosts)

    def test_multiple_vhosts(self):
        content = """
          server {
            server_name www.domain1.com;
            access_log logs/domain1.access.log main;
    
            root /var/www/domain1.com/htdocs;
          }
    
          server {
            server_name www.domain2.com;
            access_log  logs/domain2.access.log main;
    
            root /var/www/domain2.com/htdocs;
          }
          
          server {
            listen 80;
            server_name www.example4.com;
            error_log   /var/log/nginx/www.XYZ-web-testing-new.XYZ.cz_error.log;
            access_log  /var/log/nginx/www.XYZ-web-testing-new.XYZ.cz_access.log apm;
        
            return 301 https://www.XYZ-web-testing-new.XYZ.cz$request_uri;
          }
        
        server {
            listen 443 ssl http2;
            server_name www.example3.com;
        
            location / {
                proxy_pass http://localhost:4001;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_redirect off;
            }
            location ~ (/adminer/|/adminer$) {
                allow 10.0.0.0/8;
                allow 172.16.0.0/12;
                allow 192.168.0.0/16;
                allow 127.0.0.1/8;
                allow ::1/128;
                deny all;
        
                root /var/www/adminer;
                index index.php;
                location ~* \.php$ {
                    fastcgi_split_path_info ^(.+\.php)(/.+)$;
                    fastcgi_pass unix:/var/run/php/www.sock;
                    fastcgi_index index.php;
                    include fastcgi_params;
                }
            }
        
        }
        """
        expected_vhosts = {'www.domain1.com', 'www.domain2.com', 'www.example3.com', 'www.example4.com'}
        result_vhosts = self.cmds.get_all_vhosts_from_content(content)
        self.assertSetEqual(expected_vhosts, result_vhosts)

    def test_localhost1(self):
        content = """
        http {
          index index.html;

          server {
            server_name localhost 127.0.0.1;
            access_log logs/domain1.access.log main;

            root /var/www/domain1.com/htdocs;
          }
        }
        """
        expected_vhosts = {'localhost', '127.0.0.1'}
        result_vhosts = self.cmds.get_all_vhosts_from_content(content)
        self.assertSetEqual(expected_vhosts, result_vhosts)

    def test_localhost2(self):
        content = """
        http {
          index index.html;

          server {
            server_name 127.0.0.1 localhost;
            access_log logs/domain1.access.log main;

            root /var/www/domain1.com/htdocs;
          }
        }
        """
        expected_vhosts = {'localhost', '127.0.0.1'}
        result_vhosts = self.cmds.get_all_vhosts_from_content(content)
        self.assertSetEqual(expected_vhosts, result_vhosts)

    def test_example1(self):
        content = """
        http {
          index index.html;
        
          server {
            server_name www.domain1.com;
            access_log logs/domain1.access.log main;
        
            root /var/www/domain1.com/htdocs;
          }
        
          server {
            server_name www.domain2.com;
            access_log  logs/domain2.access.log main;
        
            root /var/www/domain2.com/htdocs;
          }
        }
        """
        expected_vhosts = {'www.domain1.com', 'www.domain2.com'}
        result_vhosts = self.cmds.get_all_vhosts_from_content(content)
        self.assertSetEqual(expected_vhosts, result_vhosts)

    def test_example2(self):
        content = """
        server {
            listen 80;
            server_name localhost 127.0.0.1;
        
            location ~ ^/(status|ping)$ {
              access_log off;
        
              allow 127.0.0.1;
              deny all;
        
              fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
              fastcgi_index index.php;
            }
        }
        
        server {
            listen 80;
            server_name sub.example1.cz;
            root /var/www/sub.example1.cz;
        
            error_log   /var/log/nginx/sub.example1.cz_error.log;
            access_log  /var/log/nginx/sub.example1.cz_access.log apm;
        
            return 301 https://www.example1.cz$request_uri;
        }
        server {
            listen 443 ssl http2;
            server_name sub.example2.cz;
        
        
            ssl on;
            ssl_protocols TLSv1.2 TLSv1.3;
            ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;
            ssl_prefer_server_ciphers off;
            ssl_session_timeout 1d;
        
        }
        
        
        server {
            listen 80;
            server_name sub.example4.cz;
            root /var/www/html;
        
            return 301 https://www.sub.example4.cz$request_uri;
        }
        
        server {
            listen 443 ssl http2;
            server_name sub.example4.cz;
        
            return 301 https://www.sub.example4.cz$request_uri;
        }
        
        server {
            listen 80;
            server_name sub.example3.cz;
        
            return 301 https://www.google.com;
        }
        server {
            listen 443 ssl http2;
            server_name www.sub.example5.cz;
        
        
            ssl on;
            ssl_protocols TLSv1.2 TLSv1.3;
            ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;
            ssl_prefer_server_ciphers off;
            ssl_session_cache shared:SSL:10m;
        
            ssl_certificate     /etc/ssl/private/certmach_sub.example5.cz_fullchain.pem;
            ssl_certificate_key /etc/ssl/private/certmach_sub.example5.cz.pem;
            ssl_session_timeout 1d;
            ssl_session_tickets off;
            ssl_dhparam /etc/ssl/ffdhe2048.txt;
            location / {
                proxy_pass http://localhost:1339;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header X-Forwarded-Host $http_host;
                proxy_set_header Host $http_host;
                proxy_set_header X-NginX-Proxy true;
        
                # Enables WS support
                proxy_http_version 1.1;
                proxy_set_header Upgrade $http_upgrade;
                proxy_set_header Connection "upgrade";
                proxy_redirect off;
            }
            location ~ (/adminer/|/adminer$) {
                allow 10.0.0.0/8;
                allow 172.16.0.0/12;
                allow 192.168.0.0/16;
                allow 127.0.0.1/8;
                allow ::1/128;
                deny all;
        
                root /var/www/adminer;
                index index.php;
                location ~* \.php$ {
                    fastcgi_split_path_info ^(.+\.php)(/.+)$;
                    fastcgi_pass unix:/var/run/php/www.sock;
                    fastcgi_index index.php;
                    fastcgi_param SCRIPT_FILENAME /var/www/adminer$fastcgi_script_name;
                    fastcgi_param QUERY_STRING $query_string;
                    include fastcgi_params;
                }
            }
        }
        """
        expected_vhosts = {'localhost', '127.0.0.1', 'sub.example1.cz', 'sub.example2.cz', 'sub.example3.cz',
                           'sub.example4.cz', 'www.sub.example5.cz'}
        result_vhosts = self.cmds.get_all_vhosts_from_content(content)
        self.assertSetEqual(expected_vhosts, result_vhosts)


