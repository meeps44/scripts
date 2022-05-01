import socket

# Performs IPv6 DNS-lookup on a given list of hostnames and logs the resulting IPv6-addresses to a file
#filename = "ipv6-address-list-full-alexa-top500.txt"
filename = "nslookup-alexa-top500.txt"
filename_www = "nslookup-alexa-top500-www.txt"
filename_full = "nslookup-alexa-top500-full.txt"

hostnames_long = [
		"google.com",
		"youtube.com",
		"facebook.com",
		"baidu.com",
		"instagram.com",
		"bilibili.com",
		"wikipedia.org",
		"amazon.com",
		"qq.com",
		"twitter.com",
		"whatsapp.com",
		"yahoo.com",
		"zhihu.com",
		"linkedin.com",
		"reddit.com",
		"live.com",
		"google.com.hk",
		"csdn.net",
		"bing.com",
		"github.com",
		"taobao.com",
		"zoom.us",
		"office.com",
		"microsoft.com",
		"yandex.ru",
		"163.com",
		"sina.com.cn",
		"weibo.com",
		"vk.com",
		"xvideos.com",
		"tiktok.com",
		"jd.com",
		"stackoverflow.com",
		"pornhub.com",
		"canva.com",
		"sohu.com",
		"aliexpress.com",
		"microsoftonline.com",
		"paypal.com",
		"yahoo.co.jp",
		"myshopify.com",
		"amazon.in",
		"naver.com",
		"fandom.com",
		"netflix.com",
		"mail.ru",
		"douban.com",
		"t.co",
		"1688.com",
		"tmall.com",
		"apple.com",
		"quora.com",
		"xhamster.com",
		"ebay.com",
		"imdb.com",
		"google.co.in",
		"adobe.com",
		"cnblogs.com",
		"google.cn",
		"twitch.tv",
		"spankbang.com",
		"duckduckgo.com",
		"indeed.com",
		"alibaba.com",
		"msn.com",
		"discord.com",
		"hao123.com",
		"flipkart.com",
		"coinmarketcap.com",
		"alipay.com",
		"pinterest.com",
		"telegram.org",
		"etsy.com",
		"wordpress.com",
		"xnxx.com",
		"tencent.com",
		"amazon.co.jp",
		"amazonaws.com",
		"pixiv.net",
		"imgur.com",
		"sogou.com",
		"nytimes.com",
		"booking.com",
		"ilovepdf.com",
		"t.me",
		"freepik.com",
		"jianshu.com",
		"dropbox.com",
		"tumblr.com",
		"cnn.com",
		"medium.com",
		"aliyun.com",
		"bbc.com",
		"wetransfer.com",
		"spotify.com",
		"tradingview.com",
		"twimg.com",
		"force.com",
		"mediafire.com",
		"chaturbate.com",
		"feishu.cn",
		"fiverr.com",
		"eastmoney.com",
		"w3schools.com",
		"hupu.com",
		"smzdm.com",
		"realsrv.com",
		"digikala.com",
		"douyu.com",
		"youku.com",
		"ok.ru",
		"mega.nz",
		"amazon.co.uk",
		"walmart.com",
		"avito.ru",
		"instructure.com",
		"trello.com",
		"indiatimes.com",
		"3dmgame.com",
		"xiaohongshu.com",
		"grammarly.com",
		"atlassian.net",
		"youdao.com",
		"thepaper.cn",
		"office365.com",
		"so.com",
		"rakuten.co.jp",
		"zillow.com",
		"vimeo.com",
		"binance.com",
		"360.cn",
		"weather.com",
		"udemy.com",
		"amazon.de",
		"godaddy.com",
		"dailymail.co.uk",
		"slack.com",
		"dcinside.com",
		"savefrom.net",
		"iqiyi.com",
		"behance.net",
		"gosuslugi.ru",
		"hotstar.com",
		"espn.com",
		"archive.org",
		"nih.gov",
		"deepl.com",
		"uol.com.br",
		"amazon.ca",
		"patreon.com",
		"zerodha.com",
		"theguardian.com",
		"google.co.jp",
		"daum.net",
		"cnki.net",
		"cloudfront.net",
		"okta.com",
		"nga.cn",
		"shutterstock.com",
		"google.ru",
		"fc2.com",
		"shopify.com",
		"mercadolivre.com.br",
		"chase.com",
		"amazon.it",
		"nicovideo.jp",
		"roblox.com",
		"hdfcbank.com",
		"google.fr",
		"googlevideo.com",
		"ifeng.com",
		"tistory.com",
		"quizlet.com",
		"linktr.ee",
		"investing.com",
		"google.com.tw",
		"researchgate.net",
		"bbc.co.uk",
		"speedtest.net",
		"sciencedirect.com",
		"blogger.com",
		"mozilla.org",
		"globo.com",
		"marca.com",
		"line.me",
		"zoho.com",
		"zhibo8.cc",
		"upwork.com",
		"deviantart.com",
		"y2mate.com",
		"yandex.com",
		"douyin.com",
		"dmm.co.jp",
		"ozon.ru",
		"messenger.com",
		"stackexchange.com",
		"hubspot.com",
		"salesforce.com",
		"gamersky.com",
		"steampowered.com",
		"onlyfans.com",
		"cctv.com",
		"primevideo.com",
		"amazon.es",
		"amazon.fr",
		"google.es",
		"ali213.net",
		"360doc.com",
		"pconline.com.cn",
		"notion.so",
		"smallpdf.com",
		"jb51.net",
		"animeflv.net",
		"totalwownews.com",
		"samsung.com",
		"xueqiu.com",
		"fedex.com",
		"healthline.com",
		"geeksforgeeks.org",
		"9gag.com",
		"autohome.com.cn",
		"homedepot.com",
		"huaban.com",
		"google.ca",
		"runoob.com",
		"huya.com",
		"ikea.com",
		"craigslist.org",
		"bankofamerica.com",
		"shopee.tw",
		"livedoor.jp",
		"wix.com",
		"yts.mx",
		"envato.com",
		"bet365.com",
		"huawei.com",
		"aliyundrive.com",
		"opensea.io",
		"zendesk.com",
		"52pojie.cn",
		"pexels.com",
		"google.com.tr",
		"nhentai.net",
		"wildberries.ru",
		"mangaraw.co",
		"cnbc.com",
		"foxnews.com",
		"usps.com",
		"figma.com",
		"namu.wiki",
		"cricbuzz.com",
		"google.de",
		"google.com.sg",
		"ups.com",
		"bendibao.com",
		"5ch.net",
		"shaparak.ir",
		"wordpress.org",
		"aliyuncs.com",
		"soundcloud.com",
		"bitly.com",
		"aliexpress.ru",
		"scribd.com",
		"toutiao.com",
		"lazada.sg",
		"intuit.com",
		"stripe.com",
		"juejin.cn",
		"mercadolibre.com.mx",
		"google.com.br",
		"pixabay.com",
		"rt.com",
		"e-hentai.org",
		"nyaa.si",
		"varzesh3.com",
		"docin.com",
		"coupang.com",
		"qidian.com",
		"hitomi.la",
		"goodreads.com",
		"aparat.com",
		"google.co.uk",
		"alibaba-inc.com",
		"google.com.mx",
		"tokopedia.com",
		"reverso.net",
		"unsplash.com",
		"51cto.com",
		"gitee.com",
		"btsow.rest",
		"ctrip.com",
		"sxyprn.com",
		"amazon.com.mx",
		"asana.com",
		"onlinesbi.com",
		"istockphoto.com",
		"hp.com",
		"ixigua.com",
		"as.com",
		"zol.com.cn",
		"zippyshare.com",
		"redd.it",
		"moneycontrol.com",
		"ria.ru",
		"remove.bg",
		"indiamart.com",
		"sahibinden.com",
		"reuters.com",
		"themeforest.net",
		"yuque.com",
		"shein.com",
		"readmanganato.com",
		"canada.ca",
		"wellsfargo.com",
		"coursera.org",
		"slideshare.net",
		"taboola.com",
		"forbes.com",
		"bloomberg.com",
		"mailchimp.com",
		"17track.net",
		"wayfair.com",
		"naukri.com",
		"kakao.com",
		"fast.com",
		"irctc.co.in",
		"dailymotion.com",
		"wp.pl",
		"dell.com",
		"myworkday.com",
		"daftsex.com",
		"book118.com",
		"trendyol.com",
		"quillbot.com",
		"soso.com",
		"alicdn.com",
		"google.com.sa",
		"dingtalk.com",
		"shopee.com.my",
		"blog.jp",
		"bestbuy.com",
		"t66y.com",
		"businessinsider.com",
		"shopee.co.id",
		"www.gov.uk",
		"youporn.com",
		"yelp.com",
		"eporner.com",
		"eksisozluk.com",
		"cloudflare.com",
		"target.com",
		"icicibank.com",
		"gsmarena.com",
		"hulu.com",
		"atlassian.com",
		"flickr.com",
		"acfun.cn",
		"americanexpress.com",
		"pinimg.com",
		"udn.com",
		"zcool.com.cn",
		"gismeteo.ru",
		"google.co.th",
		"gstatic.com",
		"ameblo.jp",
		"wsj.com",
		"google.com.ar",
		"guancha.cn",
		"4chan.org",
		"tripadvisor.com",
		"v2ex.com",
		"airbnb.com",
		"2345.com",
		"xhamsterlive.com",
		"91porn.com",
		"dribbble.com",
		"capitalone.com",
		"torob.com",
		"hepsiburada.com",
		"box.com",
		"mercadolibre.com.ar",
		"ettoday.net",
		"chaoxing.com",
		"steamcommunity.com",
		"ptt.cc",
		"divar.ir",
		"gogoanime.sk",
		"kdocs.cn",
		"blackboard.com",
		"skype.com",
		"myworkdayjobs.com",
		"nike.com",
		"wikimedia.org",
		"gearbest.com",
		"chegg.com",
		"chess.com",
		"cambridge.org",
		"genius.com",
		"tapd.cn",
		"codegrepper.com",
		"accuweather.com",
		"ouo.io",
		"ebay.co.uk",
		"iqbroker.com",
		"investopedia.com",
		"fidelity.com",
		"sinaimg.cn",
		"espncricinfo.com",
		"stripchat.com",
		"glassdoor.com",
		"lenta.ru",
		"noodlemagazine.com",
		"archiveofourown.org",
		"fmkorea.com",
		"onet.pl",
		"google.com.au",
		"disneyplus.com",
		"azure.com",
		"manage.wix.com",
		"wikihow.com",
		"makemytrip.com",
		"crunchyroll.com",
		"xervoo.net",
		"cnbeta.com",
		"nypost.com",
		"sina.cn",
		"asus.com",
		"merriam-webster.com",
		"google.pl",
		"lanzoug.com",
		"realtor.com",
		"livejournal.com",
		"mit.edu",
		"doc88.com",
		"icloud.com",
		"agacelebir.com",
		"inven.co.kr",
		"dhl.com",
		"mlb.com",
		"infobae.com",
		"chinaz.com",
		"ign.com",
		"myshoplaza.com",
		"washingtonpost.com",
		"storage.googleapis.com",
		"ndtv.com",
		"oracle.com",
		"kuaishou.com",
		"protonmail.com",
		"ca.gov",
		"vnexpress.net",
		"mi.com",
		"playstation.com",
		"ezgif.com",
		"livejasmin.com",
		"gamer.com.tw",
		"cunhua.shop",
		"google.az",
		"shopee.co.th",
		"shimo.im",
		"europa.eu",
		"thesaurus.com",
		"shopee.vn",
		"58.com",
		"google.co.id",
		"nba.com",
		"gamespot.com",
		"myntra.com",
		"ibm.com",
		"huaweicloud.com",
		"gamewith.jp",
		"fextralife.com",
		"marketwatch.com",
		"tianyancha.com",
		"amazon.com.au",
		"myanimelist.net",
		"weebly.com",
		"ruliweb.com",
		"sberbank.ru",
		"google.co.kr",
		"npmjs.com",
		"webmd.com",
		"baiducontent.com",
		"nextdoor.com",
		"docomo.ne.jp",
		"calendly.com",
		"eroterest.net",
		"cifnews.com",
		"interia.pl",
		"rambler.ru",
		"xfinity.com",
		"oschina.net",
		"google.com.eg",
		"news18.com",
		"costco.com",
		"woa.com",
		"wp.com",
		"quark.cn",
		"cnet.com",
		"squarespace.com"
]

hostnames_long_www = [
		"www.google.com",
		"www.youtube.com",
		"www.facebook.com",
		"www.baidu.com",
		"www.instagram.com",
		"www.bilibili.com",
		"www.wikipedia.org",
		"www.amazon.com",
		"www.qq.com",
		"www.twitter.com",
		"www.whatsapp.com",
		"www.yahoo.com",
		"www.zhihu.com",
		"www.linkedin.com",
		"www.reddit.com",
		"www.live.com",
		"www.google.com.hk",
		"www.csdn.net",
		"www.bing.com",
		"www.github.com",
		"www.taobao.com",
		"www.zoom.us",
		"www.office.com",
		"www.microsoft.com",
		"www.yandex.ru",
		"www.163.com",
		"www.sina.com.cn",
		"www.weibo.com",
		"www.vk.com",
		"www.xvideos.com",
		"www.tiktok.com",
		"www.jd.com",
		"www.stackoverflow.com",
		"www.pornhub.com",
		"www.canva.com",
		"www.sohu.com",
		"www.aliexpress.com",
		"www.microsoftonline.com",
		"www.paypal.com",
		"www.yahoo.co.jp",
		"www.myshopify.com",
		"www.amazon.in",
		"www.naver.com",
		"www.fandom.com",
		"www.netflix.com",
		"www.mail.ru",
		"www.douban.com",
		"www.t.co",
		"www.1688.com",
		"www.tmall.com",
		"www.apple.com",
		"www.quora.com",
		"www.xhamster.com",
		"www.ebay.com",
		"www.imdb.com",
		"www.google.co.in",
		"www.adobe.com",
		"www.cnblogs.com",
		"www.google.cn",
		"www.twitch.tv",
		"www.spankbang.com",
		"www.duckduckgo.com",
		"www.indeed.com",
		"www.alibaba.com",
		"www.msn.com",
		"www.discord.com",
		"www.hao123.com",
		"www.flipkart.com",
		"www.coinmarketcap.com",
		"www.alipay.com",
		"www.pinterest.com",
		"www.telegram.org",
		"www.etsy.com",
		"www.wordpress.com",
		"www.xnxx.com",
		"www.tencent.com",
		"www.amazon.co.jp",
		"www.amazonaws.com",
		"www.pixiv.net",
		"www.imgur.com",
		"www.sogou.com",
		"www.nytimes.com",
		"www.booking.com",
		"www.ilovepdf.com",
		"www.t.me",
		"www.freepik.com",
		"www.jianshu.com",
		"www.dropbox.com",
		"www.tumblr.com",
		"www.cnn.com",
		"www.medium.com",
		"www.aliyun.com",
		"www.bbc.com",
		"www.wetransfer.com",
		"www.spotify.com",
		"www.tradingview.com",
		"www.twimg.com",
		"www.force.com",
		"www.mediafire.com",
		"www.chaturbate.com",
		"www.feishu.cn",
		"www.fiverr.com",
		"www.eastmoney.com",
		"www.w3schools.com",
		"www.hupu.com",
		"www.smzdm.com",
		"www.realsrv.com",
		"www.digikala.com",
		"www.douyu.com",
		"www.youku.com",
		"www.ok.ru",
		"www.mega.nz",
		"www.amazon.co.uk",
		"www.walmart.com",
		"www.avito.ru",
		"www.instructure.com",
		"www.trello.com",
		"www.indiatimes.com",
		"www.3dmgame.com",
		"www.xiaohongshu.com",
		"www.grammarly.com",
		"www.atlassian.net",
		"www.youdao.com",
		"www.thepaper.cn",
		"www.office365.com",
		"www.so.com",
		"www.rakuten.co.jp",
		"www.zillow.com",
		"www.vimeo.com",
		"www.binance.com",
		"www.360.cn",
		"www.weather.com",
		"www.udemy.com",
		"www.amazon.de",
		"www.godaddy.com",
		"www.dailymail.co.uk",
		"www.slack.com",
		"www.dcinside.com",
		"www.savefrom.net",
		"www.iqiyi.com",
		"www.behance.net",
		"www.gosuslugi.ru",
		"www.hotstar.com",
		"www.espn.com",
		"www.archive.org",
		"www.nih.gov",
		"www.deepl.com",
		"www.uol.com.br",
		"www.amazon.ca",
		"www.patreon.com",
		"www.zerodha.com",
		"www.theguardian.com",
		"www.google.co.jp",
		"www.daum.net",
		"www.cnki.net",
		"www.cloudfront.net",
		"www.okta.com",
		"www.nga.cn",
		"www.shutterstock.com",
		"www.google.ru",
		"www.fc2.com",
		"www.shopify.com",
		"www.mercadolivre.com.br",
		"www.chase.com",
		"www.amazon.it",
		"www.nicovideo.jp",
		"www.roblox.com",
		"www.hdfcbank.com",
		"www.google.fr",
		"www.googlevideo.com",
		"www.ifeng.com",
		"www.tistory.com",
		"www.quizlet.com",
		"www.linktr.ee",
		"www.investing.com",
		"www.google.com.tw",
		"www.researchgate.net",
		"www.bbc.co.uk",
		"www.speedtest.net",
		"www.sciencedirect.com",
		"www.blogger.com",
		"www.mozilla.org",
		"www.globo.com",
		"www.marca.com",
		"www.line.me",
		"www.zoho.com",
		"www.zhibo8.cc",
		"www.upwork.com",
		"www.deviantart.com",
		"www.y2mate.com",
		"www.yandex.com",
		"www.douyin.com",
		"www.dmm.co.jp",
		"www.ozon.ru",
		"www.messenger.com",
		"www.stackexchange.com",
		"www.hubspot.com",
		"www.salesforce.com",
		"www.gamersky.com",
		"www.steampowered.com",
		"www.onlyfans.com",
		"www.cctv.com",
		"www.primevideo.com",
		"www.amazon.es",
		"www.amazon.fr",
		"www.google.es",
		"www.ali213.net",
		"www.360doc.com",
		"www.pconline.com.cn",
		"www.notion.so",
		"www.smallpdf.com",
		"www.jb51.net",
		"www.animeflv.net",
		"www.totalwownews.com",
		"www.samsung.com",
		"www.xueqiu.com",
		"www.fedex.com",
		"www.healthline.com",
		"www.geeksforgeeks.org",
		"www.9gag.com",
		"www.autohome.com.cn",
		"www.homedepot.com",
		"www.huaban.com",
		"www.google.ca",
		"www.runoob.com",
		"www.huya.com",
		"www.ikea.com",
		"www.craigslist.org",
		"www.bankofamerica.com",
		"www.shopee.tw",
		"www.livedoor.jp",
		"www.wix.com",
		"www.yts.mx",
		"www.envato.com",
		"www.bet365.com",
		"www.huawei.com",
		"www.aliyundrive.com",
		"www.opensea.io",
		"www.zendesk.com",
		"www.52pojie.cn",
		"www.pexels.com",
		"www.google.com.tr",
		"www.nhentai.net",
		"www.wildberries.ru",
		"www.mangaraw.co",
		"www.cnbc.com",
		"www.foxnews.com",
		"www.usps.com",
		"www.figma.com",
		"www.namu.wiki",
		"www.cricbuzz.com",
		"www.google.de",
		"www.google.com.sg",
		"www.ups.com",
		"www.bendibao.com",
		"www.5ch.net",
		"www.shaparak.ir",
		"www.wordpress.org",
		"www.aliyuncs.com",
		"www.soundcloud.com",
		"www.bitly.com",
		"www.aliexpress.ru",
		"www.scribd.com",
		"www.toutiao.com",
		"www.lazada.sg",
		"www.intuit.com",
		"www.stripe.com",
		"www.juejin.cn",
		"www.mercadolibre.com.mx",
		"www.google.com.br",
		"www.pixabay.com",
		"www.rt.com",
		"www.e-hentai.org",
		"www.nyaa.si",
		"www.varzesh3.com",
		"www.docin.com",
		"www.coupang.com",
		"www.qidian.com",
		"www.hitomi.la",
		"www.goodreads.com",
		"www.aparat.com",
		"www.google.co.uk",
		"www.alibaba-inc.com",
		"www.google.com.mx",
		"www.tokopedia.com",
		"www.reverso.net",
		"www.unsplash.com",
		"www.51cto.com",
		"www.gitee.com",
		"www.btsow.rest",
		"www.ctrip.com",
		"www.sxyprn.com",
		"www.amazon.com.mx",
		"www.asana.com",
		"www.onlinesbi.com",
		"www.istockphoto.com",
		"www.hp.com",
		"www.ixigua.com",
		"www.as.com",
		"www.zol.com.cn",
		"www.zippyshare.com",
		"www.redd.it",
		"www.moneycontrol.com",
		"www.ria.ru",
		"www.remove.bg",
		"www.indiamart.com",
		"www.sahibinden.com",
		"www.reuters.com",
		"www.themeforest.net",
		"www.yuque.com",
		"www.shein.com",
		"www.readmanganato.com",
		"www.canada.ca",
		"www.wellsfargo.com",
		"www.coursera.org",
		"www.slideshare.net",
		"www.taboola.com",
		"www.forbes.com",
		"www.bloomberg.com",
		"www.mailchimp.com",
		"www.17track.net",
		"www.wayfair.com",
		"www.naukri.com",
		"www.kakao.com",
		"www.fast.com",
		"www.irctc.co.in",
		"www.dailymotion.com",
		"www.wp.pl",
		"www.dell.com",
		"www.myworkday.com",
		"www.daftsex.com",
		"www.book118.com",
		"www.trendyol.com",
		"www.quillbot.com",
		"www.soso.com",
		"www.alicdn.com",
		"www.google.com.sa",
		"www.dingtalk.com",
		"www.shopee.com.my",
		"www.blog.jp",
		"www.bestbuy.com",
		"www.t66y.com",
		"www.businessinsider.com",
		"www.shopee.co.id",
		"www.www.gov.uk",
		"www.youporn.com",
		"www.yelp.com",
		"www.eporner.com",
		"www.eksisozluk.com",
		"www.cloudflare.com",
		"www.target.com",
		"www.icicibank.com",
		"www.gsmarena.com",
		"www.hulu.com",
		"www.atlassian.com",
		"www.flickr.com",
		"www.acfun.cn",
		"www.americanexpress.com",
		"www.pinimg.com",
		"www.udn.com",
		"www.zcool.com.cn",
		"www.gismeteo.ru",
		"www.google.co.th",
		"www.gstatic.com",
		"www.ameblo.jp",
		"www.wsj.com",
		"www.google.com.ar",
		"www.guancha.cn",
		"www.4chan.org",
		"www.tripadvisor.com",
		"www.v2ex.com",
		"www.airbnb.com",
		"www.2345.com",
		"www.xhamsterlive.com",
		"www.91porn.com",
		"www.dribbble.com",
		"www.capitalone.com",
		"www.torob.com",
		"www.hepsiburada.com",
		"www.box.com",
		"www.mercadolibre.com.ar",
		"www.ettoday.net",
		"www.chaoxing.com",
		"www.steamcommunity.com",
		"www.ptt.cc",
		"www.divar.ir",
		"www.gogoanime.sk",
		"www.kdocs.cn",
		"www.blackboard.com",
		"www.skype.com",
		"www.myworkdayjobs.com",
		"www.nike.com",
		"www.wikimedia.org",
		"www.gearbest.com",
		"www.chegg.com",
		"www.chess.com",
		"www.cambridge.org",
		"www.genius.com",
		"www.tapd.cn",
		"www.codegrepper.com",
		"www.accuweather.com",
		"www.ouo.io",
		"www.ebay.co.uk",
		"www.iqbroker.com",
		"www.investopedia.com",
		"www.fidelity.com",
		"www.sinaimg.cn",
		"www.espncricinfo.com",
		"www.stripchat.com",
		"www.glassdoor.com",
		"www.lenta.ru",
		"www.noodlemagazine.com",
		"www.archiveofourown.org",
		"www.fmkorea.com",
		"www.onet.pl",
		"www.google.com.au",
		"www.disneyplus.com",
		"www.azure.com",
		"www.manage.wix.com",
		"www.wikihow.com",
		"www.makemytrip.com",
		"www.crunchyroll.com",
		"www.xervoo.net",
		"www.cnbeta.com",
		"www.nypost.com",
		"www.sina.cn",
		"www.asus.com",
		"www.merriam-webster.com",
		"www.google.pl",
		"www.lanzoug.com",
		"www.realtor.com",
		"www.livejournal.com",
		"www.mit.edu",
		"www.doc88.com",
		"www.icloud.com",
		"www.agacelebir.com",
		"www.inven.co.kr",
		"www.dhl.com",
		"www.mlb.com",
		"www.infobae.com",
		"www.chinaz.com",
		"www.ign.com",
		"www.myshoplaza.com",
		"www.washingtonpost.com",
		"www.storage.googleapis.com",
		"www.ndtv.com",
		"www.oracle.com",
		"www.kuaishou.com",
		"www.protonmail.com",
		"www.ca.gov",
		"www.vnexpress.net",
		"www.mi.com",
		"www.playstation.com",
		"www.ezgif.com",
		"www.livejasmin.com",
		"www.gamer.com.tw",
		"www.cunhua.shop",
		"www.google.az",
		"www.shopee.co.th",
		"www.shimo.im",
		"www.europa.eu",
		"www.thesaurus.com",
		"www.shopee.vn",
		"www.58.com",
		"www.google.co.id",
		"www.nba.com",
		"www.gamespot.com",
		"www.myntra.com",
		"www.ibm.com",
		"www.huaweicloud.com",
		"www.gamewith.jp",
		"www.fextralife.com",
		"www.marketwatch.com",
		"www.tianyancha.com",
		"www.amazon.com.au",
		"www.myanimelist.net",
		"www.weebly.com",
		"www.ruliweb.com",
		"www.sberbank.ru",
		"www.google.co.kr",
		"www.npmjs.com",
		"www.webmd.com",
		"www.baiducontent.com",
		"www.nextdoor.com",
		"www.docomo.ne.jp",
		"www.calendly.com",
		"www.eroterest.net",
		"www.cifnews.com",
		"www.interia.pl",
		"www.rambler.ru",
		"www.xfinity.com",
		"www.oschina.net",
		"www.google.com.eg",
		"www.news18.com",
		"www.costco.com",
		"www.woa.com",
		"www.wp.com",
		"www.quark.cn",
		"www.cnet.com",
		"www.squarespace.com"
]

hostnames_full = hostnames_long + hostnames_long_www

def dnslookup(hostname_list, filename):
	with open(filename, "w") as my_file:
		for host in hostname_list:
			try:
				addressInfo = socket.getaddrinfo(host, 80, family=socket.AF_INET6, proto=socket.IPPROTO_TCP)[0][-1][0]
				if (host == hostname_list[len(hostname_list)-1]):
					my_file.write("\'" + addressInfo + "\'")
				else:
					my_file.write("\'" + addressInfo + "\'," + "\n")
				print(host)
				print(addressInfo)
			except socket.gaierror:
				print(f"No address associated with hostname {host}")

def main():
    dnslookup(hostnames_full, filename_full)

if __name__ == "__main__":
    main()