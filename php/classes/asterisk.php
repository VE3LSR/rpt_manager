<?php
class asterisk {
    public $address;
    public $port;
    public $user;
    public $password;

    public function __construct($address, $port, $user, $password, $repeater, $description) {
        $this->address = $address;
        $this->port = $port;
        $this->user = $user;
        $this->password = $password;
        $this->repeater = $repeater;
        $this->description = $description;
    }

    public function connect() {
        $this->session = ssh2_connect($this->address, $this->port);
        if (!$this->session) return false;
        return true;
    }

    function login() {
        return ssh2_auth_password($this->session, $this->user, $this->password);
    }

    function sendCommands($commands) {
        foreach ($commands as $command) {
            print "/usr/sbin/asterisk -rx \"rpt fun " . $this->repeater . " $command\"";
            $stream = ssh2_exec($this->session, "/usr/sbin/asterisk -rx \"rpt fun " . $this->repeater . " $command\"");
            while ( !empty($buffer)) {
                $buffer = fread($stream, 4096);
                print $buffer;
                if (feof($stream)) break;
            }
        }
    }

    function logout() {
        ssh2_exec ($this->session, "exit");
    }
}
