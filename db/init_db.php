<?php
require "db.php";

try {
    $db->exec("
    CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        project_id INTEGER,
        message TEXT NOT NULL,
        date TEXT NOT NULL
    )
");
} catch (PDOException $e) {
    echo "Error creating projects table: " . $e->getMessage();
}

echo "Comments table created successfully";
