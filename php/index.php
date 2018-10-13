<?php

include "devices.php";

// Remember, devices start at offset 0!
$device = 2;
$commands = ["\#87"];

$devices[$device]->connect();
$devices[$device]->login();
$devices[$device]->setTime();
#$devices[$device]->sendCommands($commands);
$devices[$device]->logout();
