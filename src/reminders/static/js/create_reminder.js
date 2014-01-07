(function($, config) {
    $('#id_when').datetimepicker({
        startDate: new Date(),
        language: 'fr',
    });

    $('#id_phone').typeahead({
        name: 'my_contacts',
        template: function(contact) {
            return [
                '<p><strong>',
                contact.tokens[0] + ' ' + contact.tokens[1],
                '</strong>',
                '<br />',
                contact.tokens[2],
                '</p>'
            ].join('');
        },
        remote: {
            url: config.contact_url + '?query=%QUERY',
            filter: function(data) {
                var contacts = $.map(data, function(contact) {
                    return {
                        value: contact[2],
                        tokens: contact
                    };
                });
                return contacts;
            }
        }
        /*updater: function(item) {
            var regex = new RegExp('\\+[0-9]+');
            var extract = regex.exec(item);
            return extract[0];
        },*/
    });
})($, config);
