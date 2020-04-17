from goprocam import GoProCamera, constants
# import and initialise gopro
goproCamera = GoProCamera.GoPro()

# download all photos from gopro sd card
goproCamera.downloadAll()
# delete all photos from gopro sd card
goproCamera.delete("all")
