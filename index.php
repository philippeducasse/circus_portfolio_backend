<?php
header("Content-Type: application/json");

$method = $_SERVER["REQUEST_METHOD"];

if ($method === "POST") {
    $data = json_decode(file_get_contents("php://input"), true);

    $comment = [
        "name" => $data["name"] ?? "Anonymous",
        "message" => $data["message"],
        "date" => date("d-m-y H:i:s")
    ];

    echo json_decode($comment["message"]);
} else {

    echo json_encode(["message" => "Hello World!"]);
}
