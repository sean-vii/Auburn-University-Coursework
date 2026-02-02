<?php
// -------------------------------------------------------------
// Database connection settings
// -------------------------------------------------------------
$dbHost = "localhost";
$dbUser = "db_username";
$dbPass = "db_password";
$dbName = "db_name";

// -------------------------------------------------------------
// Initialize variables for use in the HTML
// -------------------------------------------------------------
$sql          = "";
$error        = "";
$message      = "";
$columnNames  = array();
$rows         = array();

// -------------------------------------------------------------
// Handle form submission
// -------------------------------------------------------------
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    // Get SQL from form
    $sql = isset($_POST["sql"]) ? trim($_POST["sql"]) : "";

    if ($sql === "") {
        $error = "Please enter an SQL statement.";
    } elseif (preg_match("/\\bdrop\\b/i", $sql)) {
        // Block DROP statements (case-insensitive, whole word)
        $error = "DROP statements are not allowed.";
    } else {
        // Connect to MySQL
        $mysqli = new mysqli($dbHost, $dbUser, $dbPass, $dbName);

        if ($mysqli->connect_errno) {
            $error = "Database connection failed: " . htmlspecialchars($mysqli->connect_error);
        } else {
            // Detect the first word of the statement (SELECT, INSERT, etc.)
            $firstToken = strtok($sql, " \n\r\t");
            $command    = strtoupper($firstToken);

            // Run the query
            $queryResult = $mysqli->query($sql);

            if ($queryResult === false) {
                // Incorrect SQL â†’ show error message
                $error = "SQL error: " . htmlspecialchars($mysqli->error);
            } else {
                // If the result is a result set (e.g., SELECT), it will be mysqli_result
                if ($queryResult instanceof mysqli_result) {
                    // Get column names
                    $fields = $queryResult->fetch_fields();
                    foreach ($fields as $field) {
                        $columnNames[] = $field->name;
                    }

                    // Fetch all rows
                    while ($row = $queryResult->fetch_assoc()) {
                        $rows[] = $row;
                    }

                    $rowCount = count($rows);
                    $message  = "Query OK. $rowCount row(s) retrieved.";

                    $queryResult->free();
                } else {
                    // Non-SELECT statements: INSERT/UPDATE/DELETE/CREATE/etc.
                    $affected = $mysqli->affected_rows;

                    switch ($command) {
                        case "INSERT":
                            if ($affected == 1) {
                                $message = "Row Inserted.";
                            } else {
                                $message = "Row(s) Inserted: $affected.";
                            }
                            break;
                        case "DELETE":
                            $message = "Row(s) Deleted: $affected.";
                            break;
                        case "UPDATE":
                            $message = "Row(s) Updated: $affected.";
                            break;
                        case "CREATE":
                        case "ALTER":
                            $message = "Table Created/Updated.";
                            break;
                        default:
                            $message = "Statement executed successfully. Affected rows: $affected.";
                            break;
                    }
                }
            }

            $mysqli->close();
        }
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Bookstore DB Interface â€“ Sean Bevensee</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 2rem;
            background: #f5f5f5;
        }
        h1 {
            margin-bottom: 0.2rem;
        }
        .subtitle {
            color: #555;
            margin-bottom: 1.5rem;
        }
        form {
            margin-bottom: 1.5rem;
        }
        textarea {
            width: 100%;
            max-width: 100%;
            box-sizing: border-box;
            font-family: "Courier New", monospace;
            font-size: 0.95rem;
            padding: 0.5rem;
        }
        button {
            margin-top: 0.5rem;
            padding: 0.4rem 1rem;
            font-size: 1rem;
        }
        .message {
            padding: 0.6rem;
            background: #e0f7e9;
            border: 1px solid #7ecf99;
            margin-bottom: 1rem;
        }
        .error {
            padding: 0.6rem;
            background: #ffe0e0;
            border: 1px solid #ff8a8a;
            margin-bottom: 1rem;
        }
        table {
            border-collapse: collapse;
            margin-top: 0.5rem;
            background: white;
        }
        th, td {
            border: 1px solid #ccc;
            padding: 0.25rem 0.6rem;
            text-align: left;
        }
        th {
            background: #eee;
        }
    </style>
</head>
<body>
    <h1>Online Bookstore Database Interface</h1>
    <div class="subtitle">Sean Bevensee, smb0207@auburn.edu</div>
    <div class="subtitle">COMP-5120 Term Project Submission</div>

    <form method="post" action="">
        <label for="sql"><strong>Enter an SQL statement:</strong></label><br>
        <textarea id="sql" name="sql" rows="6" required><?php
            echo htmlspecialchars($sql);
        ?></textarea><br>
        <button type="submit">Run SQL</button>
    </form>

    <?php if ($error !== ""): ?>
        <div class="error"><?php echo $error; ?></div>
    <?php elseif ($message !== ""): ?>
        <div class="message"><?php echo htmlspecialchars($message); ?></div>
    <?php endif; ?>

    <?php if (!empty($columnNames)): ?>
        <table>
            <thead>
                <tr>
                    <?php foreach ($columnNames as $col): ?>
                        <th><?php echo htmlspecialchars($col); ?></th>
                    <?php endforeach; ?>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($rows as $row): ?>
                    <tr>
                        <?php foreach ($columnNames as $col): ?>
                            <td><?php echo htmlspecialchars((string)$row[$col]); ?></td>
                        <?php endforeach; ?>
                    </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
    <?php endif; ?>
</body>
</html>
