odoo.define('cap_web_free_quote.estimate_insurance', function (require) {

    "use strict";
    var ajax = require('web.ajax');

    $(document).ready(function () {
        //jQuery time
        var current_fs; //fieldsets
        $(".estimate_next").click(function(){
            var self = $(this);
            var store_data_model = self.attr('data-store-model')
            if(store_data_model){
                current_fs = self.parent();
                var input_args = {};
                current_fs.find('input').each(function(){
                    input_args[$(this).context['name']] = $(this).val();
                });
                var rec_id = $('#msform').find("input[name='res_id']").val();
                ajax.jsonRpc('/insurance/estimate-form', 'call', {
                    'input_args': input_args,
                    'rec_id': rec_id,
                }).then(function (data) {
                    if(data['create']) {
                        $('#msform').find("input[name='res_id']").val(data['res_id']);
                    }
                });
            }
        });

        $(".submit_estimate").click(function() {
            console.log("Submit call");
            var rec_id = $('#msform').find("input[name='res_id']").val();
            ajax.jsonRpc('/insurance/estimate-form-done', 'call', {
                'rec_id': rec_id,
            }).then(function (data) {

            });
        });

        $('.question_radio').on('change', function(){
            var display_block = $(this).val() == 'Yes';
            var current_div = $(this).parent().parent();
            var next_visible = current_div.attr('data-next')
            if(next_visible > 0) {
                var current_next = current_div.next();
                for(var index = 0; index < next_visible; index++) {
                    if(display_block) {
                        current_next.prop('required', true);
                        current_next.css('display', 'block');
                    } else {
                        current_next.removeProp('required');
                        current_next.css('display', 'none');
                        current_next.val(current_next.defaultValue);
                    }
                    current_next = current_next.next();
                }
            }
        });

    });
});
