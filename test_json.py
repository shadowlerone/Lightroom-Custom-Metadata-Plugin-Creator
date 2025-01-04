import LRPlugin


if __name__ == "__main__":
	plugin = LRPlugin.Plugin.load('test.json')
	plugin.export()