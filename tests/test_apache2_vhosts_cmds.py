import unittest
from src.vhosts_commands.apache2_vhosts_cmds import Apache2VhostsCmds


class TestNginxVhostsCmds(unittest.TestCase):
    def setUp(self):
        self.cmds = Apache2VhostsCmds()

    def test_example1(self):
        content = """
        # Ensure that Apache listens on port 80
        Listen 80
        <VirtualHost *:80>
            DocumentRoot "/www/example1"
            ServerName www.example.com
        
            # Other directives here
        </VirtualHost>
        
        <VirtualHost *:80>
            DocumentRoot "/www/example2"
            ServerName www.example.org
        
            # Other directives here
        </VirtualHost>
        """
        expected_vhosts = {'www.example.com', 'www.example.org'}
        result_vhosts = self.cmds.get_all_vhosts_from_content(content)
        self.assertSetEqual(expected_vhosts, result_vhosts)

    def test_root_server_name(self):
        content = """
        Listen 80
        # This is the "main" server running on 172.20.30.40
        ServerName server.example.com
        DocumentRoot "/www/mainserver"
        
        <VirtualHost 172.20.30.50>
            DocumentRoot "/www/example1"
            ServerName www.example.com
        
            # Other directives here ...
        </VirtualHost>
        
        <VirtualHost 172.20.30.50>
            DocumentRoot "/www/example2"
            ServerName www.example.org
        
            # Other directives here ...
        </VirtualHost>
        """
        expected_vhosts = {'server.example.com', 'www.example.com', 'www.example.org'}
        result_vhosts = self.cmds.get_all_vhosts_from_content(content)
        self.assertSetEqual(expected_vhosts, result_vhosts)

    def test_multiple_ips(self):
        content = """
        <VirtualHost 192.168.1.1 172.20.30.40>
        DocumentRoot "/www/server1"
        ServerName server.example.com
        ServerAlias server
        </VirtualHost>
        """
        expected_vhosts = {'server.example.com'}
        result_vhosts = self.cmds.get_all_vhosts_from_content(content)
        self.assertSetEqual(expected_vhosts, result_vhosts)

    def test_example2(self):
        content = """
        Listen 172.20.30.40:80
        Listen 172.20.30.40:8080
        Listen 172.20.30.50:80
        Listen 172.20.30.50:8080
        
        <VirtualHost 172.20.30.40:80>
            DocumentRoot "/www/example1-80"
            ServerName www.example.com
        </VirtualHost>
        
        <VirtualHost 172.20.30.40:8080>
            DocumentRoot "/www/example1-8080"
            ServerName www.example.com
        </VirtualHost>
        
        <VirtualHost 172.20.30.50:80>
            DocumentRoot "/www/example2-80"
            ServerName www.example.org
        </VirtualHost>
        
        <VirtualHost 172.20.30.50:8080>
            DocumentRoot "/www/example2-8080"
            ServerName www.example.org
        </VirtualHost>
        """
        expected_vhosts = {'www.example.com', 'www.example.org'}
        result_vhosts = self.cmds.get_all_vhosts_from_content(content)
        self.assertSetEqual(expected_vhosts, result_vhosts)

    def test_example3(self):
        content = """
        Listen 80
        <VirtualHost 172.20.30.40>
            DocumentRoot "/www/example1"
            ServerName www.example.com
        </VirtualHost>
        
        <VirtualHost 172.20.30.40>
            DocumentRoot "/www/example2"
            ServerName www.example.org
        </VirtualHost>
        
        <VirtualHost 172.20.30.40>
            DocumentRoot "/www/example3"
            ServerName www.example.net
        </VirtualHost>
        
        # IP-based
        <VirtualHost 172.20.30.50>
            DocumentRoot "/www/example4"
            ServerName www.example.edu
        </VirtualHost>
        
        <VirtualHost 172.20.30.60>
            DocumentRoot "/www/example5"
            ServerName www.example.gov
        </VirtualHost>
        """
        expected_vhosts = {'www.example.com', 'www.example.net', 'www.example.org',
                           'www.example.edu', 'www.example.gov'}
        result_vhosts = self.cmds.get_all_vhosts_from_content(content)
        self.assertSetEqual(expected_vhosts, result_vhosts)

    def test_comments1(self):
        content = """
        # Ensure that Apache listens on port 80
        Listen 80
        <VirtualHost *:80>
            DocumentRoot "/www/example1"
            #ServerName www.example.com

            # Other directives here
        </VirtualHost>

        <VirtualHost *:80>
            DocumentRoot "/www/example2"
            # ServerName www.example.org

            # Other directives here
        </VirtualHost>
        """
        expected_vhosts = set()
        result_vhosts = self.cmds.get_all_vhosts_from_content(content)
        self.assertSetEqual(expected_vhosts, result_vhosts)

    def test_comments2(self):
        content = """
        # Ensure that Apache listens on port 80
        Listen 80
        <VirtualHost *:80>
            DocumentRoot "/www/example1"
            ServerName www.example.com #www.example.cz

            # Other directives here
        </VirtualHost>

        <VirtualHost *:80>
            DocumentRoot "/www/example2"
            ServerName www.example.org #  www.example.pl

            # Other directives here
        </VirtualHost>
        """
        expected_vhosts = {'www.example.com', 'www.example.org'}
        result_vhosts = self.cmds.get_all_vhosts_from_content(content)
        self.assertSetEqual(expected_vhosts, result_vhosts)