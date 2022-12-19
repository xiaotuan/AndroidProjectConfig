import ctypes

user32 = ctypes.windll.LoadLibrary("user32")
screenWidth = user32.GetSystemMetrics(0)
screenHeight = user32.GetSystemMetrics(1)

print("Screen width: " + str(screenWidth) + ", height: " + str(screenHeight))