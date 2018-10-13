<?php

include_once "classes/rlc404.php";
include_once "classes/asterisk.php";

$devices = [
// Address, Port, User, Password, Login/Repeater
new rlc404("rlc1.ve3lsr.ca", 23, "root", "PASSWORD", "1870011206", ""),
new rlc404("rlc2.ve3lsr.ca", 23, "root", "PASSWORD", "1870011206", ""),
new rlc404("rlc.ve3lsr.ca", 23, "root", "PASSWORD", "1870011206", ""),
new asterisk("asterisk.ve3lsr.ca", 333, "root", "PASSWORD", "29154", ""),
new asterisk("asterisk.ve3lsr.ca", 333, "root", "PASSWORD", "29133", "")
];

