$(document).ready(function() {
  var $clipboard = $("#clipboard-content");
  var text = $clipboard.text();

  // Links
  if (isLink(text)) {
    $clipboard.html("<a href=\"" + text + "\" target=\"blank\">" + text + "</a>");

    // Links to images
    /* if (isImage(text)) {
      $clipboard.html("<a href=\"" + text + "\" target=\"blank\"><img id=\"clipboard-image\" src=\"" + text + "\" alt=\"" + text + "\"/></a>");
    } */
  }
  // Non-links
  else {
    // Email address
    if (isEmail(text)) {
        $clipboard.html("<a href=\"mailto:" + text + "\">" + text + "</a>");
    }
    // Phone number
    if (isPhoneNumber(text)) {
        var number = handlePhoneNumber(text);
        $clipboard.html("<a href=\"tel:" + number + "\">" + text + "</a>");
    }
  }

  // Focus on the clipboard for copy and paste
  $("#clipboard *").first().focus();
});

// Regular Expression tests
function isLink(text) {
  return /^https?:\/\/w{0,3}\.?[0-9A-Za-z_\-]*\.?[0-9A-Za-z_\-]+\.\S*$/g.test(text);
}

/*function isImage(text) {
  return /^\S+\.png$|\.jpg$|\.jpeg$|\.gif$|\.tiff$|\.bmp$/g.test(text);
}*/

function isEmail(text) {
  return /^\w+@[0-9A-Za-z_\-]+\.[A-Za-z_\-\.]+$/g.test(text);
}

function isPhoneNumber(text) {
  return /^1?-?\(?\d{3}\)?\-?\s?\d{3}\-?\s?\d{4}$/g.test(text);
}

function handlePhoneNumber(text) {
  var prefix = "+1";

  if (text.length > 10 && text.substring(0, 1) === "1") {
    prefix = "+";
  }

  return prefix + text.replace(/\s|-|\(|\)/g, "");
}
