
def load(url):
    """
    Load's the json of the any lottifile animation it should only accept the file path of the animation.json file as an input
    it doesn't return anything btw 

    """

    import json
    from streamlit_lottie import st_lottie 
    with open(f"{url}","r") as file: 
        urls = json.load(file) 
    st_lottie(urls)