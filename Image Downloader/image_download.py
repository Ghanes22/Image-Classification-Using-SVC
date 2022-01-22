from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import io
from PIL import Image
import time
import sys

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
PATH = "C:/Users/Administrator/OneDrive/Documents/INI KULIAH BUKAN MAIN MAIN/Modul Python/Driver/chromedriver.exe"

wd = webdriver.Chrome(PATH, options=options)

def get_images_from_google(wd, delay, max_images,image_name):
	def scroll_down(wd):
		wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		if wd.find_elements(By.CLASS_NAME, 'qvfT1'):
			return
		time.sleep(delay)

	url = f"https://www.google.com/search?q={str(image_name)}&tbm=isch"
	wd.get(url)

	image_urls = set()
	skips = 0

	while len(image_urls) + skips < max_images:
		scroll_down(wd)

		thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")

		for img in thumbnails[len(image_urls) + skips:max_images]:
			try:
				img.click()
				time.sleep(delay)
			except:
				continue

			images = wd.find_elements(By.CLASS_NAME, "n3VNCb")
			for image in images:
				if image.get_attribute('src') in image_urls:
					max_images += 1
					skips += 1
					break

				if image.get_attribute('src') and 'http' in image.get_attribute('src'):
					image_urls.add(image.get_attribute('src'))
					print(f"Found {len(image_urls)}")

	return image_urls,image_name


def download_image(download_path, url, file_name):
	try:
		image_content = requests.get(url).content
		image_file = io.BytesIO(image_content)
		image = Image.open(image_file)
		file_path = download_path + file_name

		with open(file_path, "wb") as f:
			image.save(f, "JPEG")

		print("Success")
	except Exception as e:
		print('FAILED - ', e)

urls,image_name = get_images_from_google(wd, 1, 150, 'Chelsea islan face')

for i, url in enumerate(urls):
	download_image(f"Dataset/Not Cropped/Chelsea Islan/", url, str(i) + ".jpg")

wd.quit()