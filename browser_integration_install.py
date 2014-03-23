from .browser_integration import *


@async
def install_chromedriver():
    if sublime.platform() == 'linux':
        if sublime.arch() == 'x32':
            dl_path = 'chromedriver-linux-32'
        elif sublime.arch() == 'x64':
            dl_path = 'chromedriver-linux-64'
    elif sublime.platform() == 'windows':
        dl_path = 'chromedriver-win-32'
    elif sublime.platform() == 'osx':
        dl_path = 'chromedriver-osx-32'

    bin_name = 'chromedriver'
    bin_folder = os.path.dirname(__file__)
    bin_path = os.path.abspath(os.path.join(bin_folder, '..', bin_name))

    dl_path = 'http://sublime.apiad.net/browser-integration/'\
              'chromedriver/%s' % dl_path

    if os.path.exists(bin_path):
        print("Found `chromedriver` executable")
        print("  in '%s'" % bin_path)
    else:
        print("Downloading `chromedriver` executable")
        print("  from '%s'" % dl_path)
        print("  into '%s'" % bin_path)

        with loading("Downloading chromedriver executable."):
            from urllib.request import urlopen

            with urlopen(dl_path) as response, open(bin_path, 'wb') as f:
                f.write(response.read())

            if sublime.platform() == 'linux' or sublime.platform() == 'osx':
                os.chmod(bin_path, 511)


install_chromedriver()
