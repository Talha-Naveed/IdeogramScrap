import random
from seleniumbase import Driver
import requests
import os
import time

profile_path = "/home/talha/.config/google-chrome"

driver = Driver(
    uc=True,
    user_data_dir=profile_path,
    headless=False
    )

driver.get("http://ideogram.ai")
driver.sleep(5)

urls = [
            "http://ideogram.ai/t/explore?f=hour",
            "http://ideogram.ai/t/explore?f=day",
            "http://ideogram.ai/t/explore?f=week",
            "http://ideogram.ai/t/explore?f=month",
            "http://ideogram.ai/t/explore?f=all_time",
            "http://ideogram.ai/t/explore?f=following",
        ]

old_links = set()
while True:

    
    for ur in urls:

        new_links = set()

        driver.open(ur)
        driver.sleep(random.randint(5, 60))
        
        image_elements = driver.find_elements('img[src]')

        for img in image_elements:
            # Get the src attribute of the image element
            
            src = img.get_attribute('src')

            if src not in old_links:
                new_links.add(src)


        download_links = new_links - old_links
        if download_links:
            print(f"New image URLs: {download_links}")

        os.makedirs("images", exist_ok=True)
        
        for link in download_links:
            try:
                response = requests.get(link, stream=True)
                if response.status_code == 200:
                    content_type = response.headers.get("Content-Type", "")
                    ext = content_type.split("/")[-1] if "image" in content_type else "jpg"
                    # Create a unique file name using global_counter and a timestamp
                    unique_name = f"images/image_{global_counter}_{int(time.time())}.{ext}"
                    with open(unique_name, "wb") as f:
                        for chunk in response.iter_content(1024):
                            f.write(chunk)
                    print(f"Downloaded: {unique_name}")
                    global_counter += 1  # Increment the global counter
                else:
                    print(f"Failed ({response.status_code}): {link}")
            except Exception as e:
                print(f"Error downloading {link}: {e}")


        # Update the old links with the new ones
        old_links.update(new_links)

        

        driver.sleep(random.randint(10, 60))
