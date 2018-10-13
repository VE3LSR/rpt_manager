<?php
class rlc404 {
    public $address;
    public $port;
    public $user;
    public $password;
    public $login;

    public function __construct($address, $port, $user, $password, $login, $description) {
        $this->address = $address;
        $this->port = $port;
        $this->user = $user;
        $this->password = $password;
        $this->login = $login;
        $this->description = $description;
    }

    public function connect() {
        $this->socket = fsockopen($this->address, $this->port);
        if (!$this->socket) return false;
        stream_set_blocking($this->socket, 0);
        return true;
    }

    function login() {
        while (!feof($this->socket)) {
            $buffer = fgets ($this->socket, 128);
            printf("$buffer");
            if ( strpos($buffer, "login:") !== false ) {
                fputs($this->socket, $this->user . "\r\n");
            }
            if ( strpos($buffer, "Password:") !== false ) {
                fputs($this->socket, $this->password . "\r\n");
            }
            if ( strpos($buffer, "~>") !== false ) {
                fputs($this->socket, "client\r\n");
            }
            if ( strpos($buffer, "DSP4") !== false ) {
                fputs($this->socket, $this->login . "\r\n");
            }
            if ( strpos($buffer, "is logged in") !== false ) {
                break;
            }
        }
    }

    function sendCommands($commands) {
        fputs($this->socket, "\r\n");
        $command = 0;
        while (!feof($this->socket)) {
            $buffer = fgets ($this->socket, 128);
            printf("$buffer");
            if ( strpos($buffer, "DSP4") !== false && $command < sizeof($commands) ) {
                fputs($this->socket, $commands[$command] . "\r\n");
                $buffer = "";
                $command++;
            }
            if ( strpos($buffer, "DSP4") !== false && $command >= sizeof($commands) ) {
                break;
            }

        }
    }

    function setTime() {
        $time = date("hi");
        $PM = (date("A") =="AM") ? 0 : 1;
        $command[0] = "025" . $time . "" . $PM;
        print($command[0]);
        $this->sendCommands($command);
    }

    function logout() {
        fputs($this->socket, "\r\n");
        while (!feof($this->socket)) {
            $buffer = fgets($this->socket, 128);
            printf("$buffer");
            if ( strpos($buffer, "DSP4") !== false ) {
                fputs($this->socket, "\030\r\n");
            }
            if ( strpos($buffer, "~>") !== false ) {
                fputs($this->socket, "exit\r\n");
            }
        }
    }
}
