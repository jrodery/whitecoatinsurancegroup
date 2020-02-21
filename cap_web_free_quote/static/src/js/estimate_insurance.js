odoo.define('cap_web_free_quote.estimate_insurance', function (require) {
    "use strict";
    var ajax = require('web.ajax');

    $(document).ready(function () {
        //jQuery time
        var current_fs; //fieldsets
        $(".estimate_next").click(function(){
            var self = $(this);
            var store_data_model = self.attr('data-store-model');
            if(store_data_model){
                current_fs = self.parent();
                var element = '';
                var input_args = {};
                var inp_data = '';
                current_fs.find('input').each(function(){
                    element = $(this);
                    inp_data = element.val();
                    if(element.hasClass('input-date-save')) {
                        inp_data = inp_data.split("/");
                        inp_data = inp_data[2].trim() + '-' + inp_data[0].trim() + '-' + inp_data[1].trim();
                    }
                    input_args[element.context['name']] = inp_data;
                });
                current_fs.find('select').each(function(){
                    input_args[$(this).context['name']] = $(this).val();
                });
                current_fs.find('textarea').each(function(){
                    input_args[$(this).context['name']] = $(this).val();
                });
                var rec_id = $('#msform').find("input[name='res_id']").val();
                var return_val = self.attr('data-return');
                var route = self.attr('data-route');
                var form  = $('#msform').parent();
                ajax.jsonRpc(route, 'call', {
                    'input_args': input_args,
                    'rec_id': rec_id,
                    'store_data_model': store_data_model,
                    'return_val': return_val
                }).then(function (data) {
                    if(data['create']) {
                        $('#msform').find("input[name='res_id']").val(data['res_id']);
                    }
                    if(return_val == 'total_insurance') {
                        form.next().find('.total_insurance')
                        .html(data['total_insurance']
                        .toLocaleString('en-EN', {
                            style: 'currency',
                            currency: 'USD'
                        }));
                    }
                });
            }
        });

        $(".submit_estimate").click(function() {
            var self = $(this);
            var rec_id = $('#msform').find("input[name='res_id']").val();
            var store_data_model = self.attr('data-store-model');
            var route = self.attr('data-route');
            ajax.jsonRpc(route, 'call', {
                'rec_id': rec_id,
                'store_data_model': store_data_model,
            }).then(function (data) {
                if(data){
                    if('total_insurance' in data){
                        $('#msform').parent().next()
                        .find('.insurance_amount').html(data['total_insurance']
                        .toLocaleString('en-EN', {style: 'currency', currency: 'USD'}));
                    }
                }
            });
        });

        $("#insurance_done").on('click', function(e){
            var self = $(this);
            var rec_id = $('#msform').find("input[name='res_id']").val();
            window.location.href = "/life/insurance-done?rec_id=" + rec_id;
        });

        $('.question_radio').on('change', function() {
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
            current_div.closest("input[type='hidden']").val($(this).val());
            // current_div.prev().val($(this).val());
        });
    });
});
