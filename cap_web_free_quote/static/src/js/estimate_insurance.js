odoo.define('cap_web_free_quote.estimate_insurance', function (require) {

    "use strict";
    var ajax = require('web.ajax');

    $(document).ready(function () {
        //jQuery time
        var current_fs; //fieldsets
        $(".estimate_next").click(function(){
            var self = $(this);
            var store_data_model = self.attr('data-store-model')
            console.log("---->> data_model :: ", store_data_model)
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
                }).then(function (data){
                    if(data['create']) {
                        $('#msform').find("input[name='res_id']").val(data['res_id']);
                    }
                });
            }
        });

        $(".submit_estimate").click(function(){
            console.log("Submit call");
        });

    });
});
