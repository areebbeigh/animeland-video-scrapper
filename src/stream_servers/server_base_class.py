import os

from src.config import TimeoutConfig
from src.utils import printd

class BaseServerScraper:
    def __init__(self, driver, proxy, selectors):
        self.driver = driver
        self.proxy = proxy
        self.selectors = selectors
        self.previos_urls = []
        self.episode_fetch_timeout = TimeoutConfig.FETCHING_EPISODE_STREAM

    def _execute_js_scripts(self):
        js_libs = os.path.join(os.path.dirname(os.path.abspath(__file__)), "js")

        loadStatus_js = os.path.join(js_libs, "loadStatus.js")
        jquery_js = os.path.join(js_libs, "jquery-3.3.1.min.js")
        jquery_onMutate_js = os.path.join(js_libs, "jquery.onmutate.min.js")
        trackIframe_js = os.path.join(js_libs, "trackIframe.js")
        removeBanner_js = os.path.join(js_libs, "removeBanner.js")

        with open(loadStatus_js, "r") as f:
            loadStatus = f.read()

        with open(jquery_js, "r") as f:
            jquery = f.read()

        with open(jquery_onMutate_js, "r") as f:
            jquery_onMutate = f.read()
        
        with open(trackIframe_js, "r") as f:
            trackIframe = f.read()
        
        with open(removeBanner_js, "r") as f:
            removeBanner = f.read()
        
        self.driver.execute_script(jquery + jquery_onMutate + loadStatus + trackIframe + removeBanner)

    def search_url_in_perflogs(self, regex_objects):
        """
        Access driver performance logs and find the stream URL by matching with the
        regular expression for the server.
        """

        proxy = self.proxy.proxy

        for entry in reversed(proxy.har['log']['entries']):
            url = entry['request']['url']
            printd(url, self.previos_urls)
            if url not in self.previos_urls:
                for regex in regex_objects:
                    if regex.match(url):
                        self.previos_urls.append(url)
                        return url
        
        return ""

    def convert_to_old_form(self):
        """
        [NOT IMPLEMENTED YET]
        Anime streaming websites don't have consistent DOM structures when it comes to new
        episode releases. This method executes a JS script in the browser that attempts to
        convert the current page to an old-form page which the scrapers are originally 
        compatible with.
        """
        pass
    
    