<?php

// PHP Data Oject
$db = new PDO("sqlite:comments.db");
// :: scope resolution operator. accesses static properties or methods
$db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
