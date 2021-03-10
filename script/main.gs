function doGet(e) {
    var p = e.parameter;
    var body;
    try{
      var translatedText = LanguageApp.translate(p.text, "", p.target);
      if (translatedText) {
        body = {
          code: 200,
          text: translatedText
        };
      } else {
        body = {
          code: 400,
          text: "Bad Request"
        };
      }
    }
    catch (e){
      body = {
        code: 400,
        text: e.toString()
      }
    }
    var response = ContentService.createTextOutput();
    response.setMimeType(ContentService.MimeType.JSON);
    response.setContent(JSON.stringify(body));

    return response;
}