import time
import subprocess

def check_scraper_health():
    """Monitor scraper and restart if needed"""
    
    last_count = 0
    stall_counter = 0
    
    while True:
        try:
            # Count locations found
            result = subprocess.run(
                ['grep', '-c', '✓', 'scrape_complete_log.txt'],
                capture_output=True,
                text=True
            )
            current_count = int(result.stdout.strip()) if result.returncode == 0 else 0
            
            # Check if making progress
            if current_count == last_count:
                stall_counter += 1
                print(f"⚠️  No progress for {stall_counter * 30} seconds (stuck at {current_count} locations)")
                
                if stall_counter >= 10:  # 5 minutes of no progress
                    print("❌ Scraper appears stalled. Check scrape_complete_log.txt for errors")
                    break
            else:
                rate = (current_count - last_count) / 0.5  # per minute
                print(f"✓ Progress: {current_count} locations (+{current_count - last_count} in 30s, ~{rate:.0f}/min)")
                stall_counter = 0
                last_count = current_count
            
            # Check for errors
            error_check = subprocess.run(
                ['grep', '-i', 'error', 'scrape_complete_log.txt'],
                capture_output=True,
                text=True
            )
            if error_check.returncode == 0 and error_check.stdout:
                print(f"⚠️  Errors detected:\n{error_check.stdout[:200]}")
            
            time.sleep(30)
            
        except KeyboardInterrupt:
            print("\nMonitoring stopped")
            break
        except Exception as e:
            print(f"Error monitoring: {e}")
            time.sleep(30)

if __name__ == "__main__":
    print("Monitoring scraper health...")
    print("Press Ctrl+C to stop\n")
    check_scraper_health()
