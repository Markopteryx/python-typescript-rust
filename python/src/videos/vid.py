import asyncio
import os

import aiohttp

# Create a directory for the videos if it doesn't already exist
folder_name = "downloaded_videos"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)


# Asynchronous function to download a single video
async def download_video(session, url, file_path):
    async with session.get(url) as response:
        if response.status == 200:
            with open(file_path, "wb") as f:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    f.write(chunk)
            print(f"Downloaded {file_path}")

        else:
            print(f"Failed to download {url}")


# Asynchronous function to manage the download of all videos
async def download_all_videos():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for x in range(1, 1897):
            video_url = f"https://embed-cloudfront.wistia.com/deliveries/88364d3e91bba3230361cb09de39e03dc2b573e8.m3u8/seg-{x}-v1-a1.ts"
            file_name = f"video_{x}.ts"
            file_path = os.path.join(folder_name, file_name)
            task = asyncio.create_task(download_video(session, video_url, file_path))
            tasks.append(task)
        await asyncio.gather(*tasks)


# Run the asynchronous download manager
asyncio.run(download_all_videos())

print("Download completed.")
