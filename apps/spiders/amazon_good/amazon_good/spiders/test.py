import re

if __name__ == "__main__":
    urls = []
    with open('G:/Python/Pythonsrc/Charlotte-master/spiders/amazon_good/amazon_good/urls.txt', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            urls.append(line.strip('\n'))

    # pattern = re.compile("\/B[^/]*[\/?]")
    # for url in urls:
    #     default = re.findall(pattern, url)
    #     if default:
    #         default = default[0]
    #         default = default.replace('/', '')
    #         default = default.replace('?', '')
    #     url = url.replace(default, 'B')
    #     print(url)
    pattern = re.compile("\/ref=[^/]*[\/?]")
    for url in urls:
        default = re.findall(pattern, url)
        if default:
            default = default[0]

            default = default.replace('/ref=', '')
            default = default.replace('?', '')
            url = url.replace(default, 'cbw_direct_from_1')
        print(url)

