# Housing Monitor

A robust Python script that monitors the STWDO housing portal for new offers and sends email alerts when available.

## Features

- ✅ Monitors housing offers every 30 seconds
- ✅ Sends email alerts when new offers are found
- ✅ Comprehensive error handling and logging
- ✅ Prevents duplicate notifications
- ✅ Robust network handling with timeouts
- ✅ Detailed logging to both console and file

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Test the script first:**
   ```bash
   python test_script.py
   ```

3. **Run the monitor:**
   ```bash
   python main.py
   ```

## Configuration

### Email Settings
The script uses Gmail SMTP. You need to:

1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password (not your regular password)
3. Update the credentials in `main.py`:
   ```python
   EMAIL_SENDER = "your-email@gmail.com"
   EMAIL_PASSWORD = "your-app-password"
   EMAIL_RECEIVER = "your-email@gmail.com"
   ```

### Monitoring Settings
- **Check interval:** 30 seconds (configurable in `main.py`)
- **URL:** STWDO housing portal (configurable)
- **Log file:** `housing_monitor.log`

## How It Works

1. **Monitoring:** The script checks the housing portal every 30 seconds
2. **Detection:** It looks for the "No results" message to determine if offers are available
3. **Alerting:** When offers are found (and no previous alert was sent), it sends an email
4. **Logging:** All activities are logged to both console and `housing_monitor.log`

## Safety Features

- **Error handling:** Network errors, parsing errors, and email errors are caught and logged
- **Timeouts:** 30-second timeout for network requests to prevent hanging
- **Duplicate prevention:** Only sends one alert per offer cycle
- **Graceful shutdown:** Handles Ctrl+C interruption properly
- **Comprehensive logging:** All activities are tracked for debugging

## Troubleshooting

### Common Issues

1. **Email authentication failed:**
   - Ensure you're using an App Password, not your regular Gmail password
   - Check that 2-factor authentication is enabled

2. **Website access issues:**
   - Check your internet connection
   - The website might be temporarily down

3. **Script crashes:**
   - Check the log file `housing_monitor.log` for error details
   - Ensure all dependencies are installed

### Log Files

- **Console output:** Real-time monitoring information
- **housing_monitor.log:** Detailed log file with timestamps

## Running in Background

### On macOS/Linux:
```bash
nohup python main.py > output.log 2>&1 &
```

### Using screen:
```bash
screen -S housing_monitor
python main.py
# Press Ctrl+A, then D to detach
# Use 'screen -r housing_monitor' to reattach
```

## Monitoring the Monitor

The script creates a log file (`housing_monitor.log`) that you can check to ensure it's running properly:

```bash
tail -f housing_monitor.log
```

## Security Notes

- Keep your email credentials secure
- The script only reads the housing website, it doesn't submit any data
- All network requests use proper headers and timeouts
- Log files may contain sensitive information (email addresses)

## Support

If you encounter issues:
1. Run `python test_script.py` to diagnose problems
2. Check the log file for error messages
3. Ensure all dependencies are installed correctly 