file_types_table = """
                <h3 style='color: #00bcd4; margin-top: 20px;'>&#128193; Supported File Types:</h3>
                <p style='color:#8b949e; font-size:12px; margin-bottom:8px;'>This application can securely wipe <b>any file type</b>. Common categories:</p>
                <table style='width:100%; border-collapse:collapse; font-size:12px; color:#c9d1d9;'>
                    <tr style='background:#1c3348;'>
                        <th style='padding:8px 10px; text-align:left;'>Category</th>
                        <th style='padding:8px 10px; text-align:left;'>Extensions</th>
                        <th style='padding:8px 10px; text-align:left;'>Use Case</th>
                    </tr>
                    <tr style='border-bottom:1px solid #1c3348;'>
                        <td style='padding:7px 10px;'>Documents</td>
                        <td style='padding:7px 10px; color:#00e676;'>.pdf .doc .docx .xls .txt .csv</td>
                        <td style='padding:7px 10px; color:#8b949e;'>Confidential reports, contracts</td>
                    </tr>
                    <tr style='border-bottom:1px solid #1c3348; background:#0a1520;'>
                        <td style='padding:7px 10px;'>Images</td>
                        <td style='padding:7px 10px; color:#00e676;'>.jpg .png .gif .bmp .raw .heic</td>
                        <td style='padding:7px 10px; color:#8b949e;'>Personal photos, scanned IDs</td>
                    </tr>
                    <tr style='border-bottom:1px solid #1c3348;'>
                        <td style='padding:7px 10px;'>Videos</td>
                        <td style='padding:7px 10px; color:#00e676;'>.mp4 .avi .mkv .mov .wmv</td>
                        <td style='padding:7px 10px; color:#8b949e;'>Recordings, surveillance footage</td>
                    </tr>
                    <tr style='border-bottom:1px solid #1c3348; background:#0a1520;'>
                        <td style='padding:7px 10px;'>Archives</td>
                        <td style='padding:7px 10px; color:#00e676;'>.zip .rar .7z .tar .iso</td>
                        <td style='padding:7px 10px; color:#8b949e;'>Compressed backups, disk images</td>
                    </tr>
                    <tr style='border-bottom:1px solid #1c3348;'>
                        <td style='padding:7px 10px;'>Code &amp; Scripts</td>
                        <td style='padding:7px 10px; color:#00e676;'>.py .js .cpp .sql .sh .bat</td>
                        <td style='padding:7px 10px; color:#8b949e;'>Source code, API keys, DB dumps</td>
                    </tr>
                    <tr style='border-bottom:1px solid #1c3348; background:#0a1520;'>
                        <td style='padding:7px 10px;'>Keys &amp; Certs</td>
                        <td style='padding:7px 10px; color:#00e676;'>.pem .key .crt .pfx .ppk</td>
                        <td style='padding:7px 10px; color:#8b949e;'>SSL certs, SSH keys, crypto wallets</td>
                    </tr>
                    <tr style='background:#0a1520;'>
                        <td style='padding:7px 10px;'>Any Other</td>
                        <td style='padding:7px 10px; color:#00e676;'>*.* (All file types)</td>
                        <td style='padding:7px 10px; color:#8b949e;'>Executables, databases, logs</td>
                    </tr>
                </table>
"""

with open('secure_wipe_desktop.py', 'r', encoding='utf-8') as f:
    content = f.read()

marker = "                <h3 style='color: #00bcd4; margin-top: 20px;'>\u2705 Compliance:</h3>"
if marker in content:
    content = content.replace(marker, file_types_table + "\n" + marker, 1)
    with open('secure_wipe_desktop.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS")
else:
    print("MARKER NOT FOUND")
    # Print nearby lines for debugging
    idx = content.find("Compliance")
    if idx > -1:
        print("Found 'Compliance' nearby:", repr(content[idx-50:idx+80]))
