/**
 * Created by Josh on 11/7/17.
 */
$(document).ready(function () {

    $('#profile-form').formValidation({
        framework: 'bootstrap',
        icon: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            steam_id: {
                validators: {
                    stringLength: {
                        min: 9,
                        max: 20,
                        message: 'The steam ID must be more than 5 and less than 20 characters long'
                    },
                    regexp: {
                        regexp: /^STEAM_[0]:[01]:\d+$/,
                        message: 'Your steam id does not match the required format. \r\nNote: use STEAM_0 even if yours is STEAM_1'
                    }
                }
            }
        }
    });
});