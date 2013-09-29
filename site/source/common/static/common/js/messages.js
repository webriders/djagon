djagon = window.djagon || {};

/* jQuery Noty modifications */
$.noty.defaults.layout = 'topCenter';

djagon.messages = {
    alert: function(text) {
        return this.message({text: text});
    },

    info: function(text) {
        return this.message({type: 'information', text: text});
    },

    warning: function(text) {
        return this.message({type: 'warning', text: text});
    },

    error: function(text) {
        return this.message({type: 'error', text: text});
    },

    success: function(text) {
        return this.message({type: 'success', text: text});
    },

    message: function(cfg) {
        return noty(cfg);
    }
};

// Handle all AJAX errors
$.ajaxSetup({
    error: function(xhr, status, error) {
        // we ignore aborted XHR or when user press F5 while XHR is in progress
        if (status == 'abort' || xhr.readyState == 0)
            return;

        var text = 'Sorry, but request has failed';
        if (error)
            text += ' (' + error + ')';

        if (xhr.responseText) {
            text = xhr.responseText;

            if (text.toLowerCase().indexOf('</html>') != -1) {
                // HTML error message will be displayed in <iframe>
                var msg = djagon.messages.message({type: 'error', layout: 'top'});
                var iframe = $('<iframe>').appendTo(msg.$message.find('.noty_text'));

                var doc = iframe.contents()[0];
                doc.open();
                doc.write(text);
                doc.close();

                var width = msg.$message.width();
                iframe.width(width);

                var height = Math.min($(doc).find('body').outerHeight(true), $(document).height());
                iframe.height(height);
            } else if (text.length > 2000) {
                // large error message
                djagon.messages.message({type: 'error', layout: 'top', text: text});
            } else {
                djagon.messages.error(text);
            }
        } else {
            djagon.messages.error(text);
        }
    }
});
