odoo.define('cap_web_free_quote.free_quote', function (require){
    "use strict";

    var ajax = require('web.ajax');

    $(document).ready(function (){
        //jQuery time
        var current_fs, next_fs, previous_fs; //fieldsets
        var left, opacity, scale; //fieldset properties which we will animate
        var animating; //flag to prevent quick multi-click glitches

        $(".format-ssn").on('keypress', function(){
            var ssn = $(this).val();
            console.log( ssn, ssn.length);

        });

        $(".format-amount").focusout(function(){
            $(this).val(Number($(this).val()).toLocaleString('en-US'));
        });

        $(".format-email").focusout(function(){
            var email = $(this).val();
            var regex = /^([a-zA-Z0-9_\.\-\+])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
            if(!regex.test(email)){
                $(this).focus();
                if(!$(this).hasClass('fill-required')){
                    $(this).addClass('fill-required');
                }
            } else {
                if($(this).hasClass('fill-required')){
                    $(this).removeClass('fill-required');
                }
            }
        });

        $('.format-phone').focusout(function(){
            $(this).val(
                $(this).val().replace(/(\d\d\d)(\d\d\d)(\d\d\d\d)/, '$1-$2-$3')
            );
        });

        $(".check_amount_format").focusout(function(){
            var str = $(this).val();
            if(!$.isNumeric(str)){
                $(this).focus();
                $(this).val('');
                $(this).attr('placeholder', 'Please follow this format. Ex.: 12345.11');
                $(this).addClass('fill-required');
            } else {
                if($(this).hasClass('fill-required')){
                    $(this).removeClass('fill-required');
                }
            }
        });

        $(".next").click(function(){
            var self = $(this);
            if(animating) return false;
            animating = true;
            var all_required_input = true;
            var all_required_textarea = true;
            var all_required_select = true;
            current_fs = self.closest('fieldset');
            next_fs = self.closest('fieldset').next();
            current_fs.find('input').each(function(){
                if($(this).prop('required') && !$(this).val().trim()){
                    all_required_input = false;
                    animating = false;
                    if(!$(this).hasClass('fill-required')){
                        $(this).addClass('fill-required');
                    }
                } else {
                    if($(this).hasClass('fill-required')){
                        $(this).removeClass('fill-required');
                    }
                }
            });
            current_fs.find('textarea').each(function(){
                if($(this).prop('required') && !$(this).val().trim()){
                    all_required_textarea = false;
                    animating = false;
                    if(!$(this).hasClass('fill-required')){
                        $(this).addClass('fill-required');
                    }
                } else {
                    if($(this).hasClass('fill-required')){
                        $(this).removeClass('fill-required');
                    }
                }
            });
            current_fs.find('select').each(function(){
                if($(this).prop('required') && !$(this).val().trim()){
                    all_required_select = false;
                    animating = false;
                    if(!$(this).hasClass('fill-required')){
                        $(this).addClass('fill-required');
                    }
                } else {
                    if($(this).hasClass('fill-required')){
                        $(this).removeClass('fill-required');
                    }
                }
            });

            if(all_required_input && all_required_textarea && all_required_select){
                //activate next step on progressbar using the index of next_fs
                $("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");
                //show the next fieldset
                next_fs.show();
                //hide the current fieldset with style
                current_fs.animate({opacity: 0},{
                    step: function(now, mx){
                        //as the opacity of current_fs reduces to 0 - stored in "now"
                        //1. scale current_fs down to 80%
                        scale = 1 - (1 - now) * 0.2;
                        //2. bring next_fs from the right(50%)
                        left = (now * 50)+"%";
                        //3. increase opacity of next_fs to 1 as it moves in
                        opacity = 1 - now;
                        current_fs.css({
                            'transform': 'scale('+scale+')',
                            'position': 'absolute'
                          });
                        next_fs.css({'left': left, 'opacity': opacity, 'position': 'relative'});
                    },
                    duration: 800,
                    complete: function(){
                        current_fs.hide();
                        animating = false;
                    },
                    //this comes from the custom easing plugin
                    easing: 'easeInOutBack'
                });
                if(self.hasClass('show_total')) {
                    $('#msform').parent().addClass('offset-md-2');
                    $('#msform').parent().removeClass('offset-md-3');
                    $('#msform').parent().next().css("display", "block");
                }

                var store_data_model = self.attr('data-store-model');
                if(store_data_model) {
                    var element = '';
                    var input_args = {};
                    var inp_data = '';
                    current_fs.find('input').each(function() {
                        element = $(this);
                        inp_data = element.val();
                        if(element.hasClass('input-date-save')) {
                            inp_data = inp_data.split("/");
                            inp_data = inp_data[2].trim() + '-' + inp_data[0].trim() + '-' + inp_data[1].trim();
                        }
                        input_args[element.context['name']] = inp_data;
                    });
                    current_fs.find('select').each(function() {
                        input_args[$(this).context['name']] = $(this).val();
                    });
                    current_fs.find('textarea').each(function() {
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
                        if(data['ref_code']) {
                            $('#msform').find("input[name='ref_code']").val(data['ref_code']);
                        }
                        if(return_val == 'total_insurance') {
                            form.next().find('.total_insurance')
                            .html(data['total_insurance']
                            .toLocaleString('en-EN', {
                                style: 'currency',
                                currency: 'USD'
                            }));
                        }
                        route = self.attr('data-route-done');
                        if(route) {
                            ajax.jsonRpc(route, 'call', {
                                'rec_id': rec_id,
                                'store_data_model': store_data_model
                            }).then(function (data) {
                                if(data) {
                                    if('total_insurance' in data) {
                                        $('#msform').parent().next()
                                            .find('.insurance_amount').html(data['total_insurance']
                                            .toLocaleString('en-EN', {style: 'currency', currency: 'USD'}));
                                    }
                                }
                            });
                        }
                    });
                }
            }
        });

        $(".previous").click(function(){
            if(animating) return false;
            animating = true;

            current_fs = $(this).parent();
            previous_fs = $(this).closest('fieldset').prev();

            //de-activate current step on progressbar
            $("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("active");

            //show the previous fieldset
            previous_fs.show();
            //hide the current fieldset with style
            current_fs.animate({opacity: 0},{
                step: function(now, mx){
                    //as the opacity of current_fs reduces to 0 - stored in "now"
                    //1. scale previous_fs from 80% to 100%
                    scale = 0.8 + (1 - now) * 0.2;
                    //2. take current_fs to the right(50%) - from 0%
                    left = ((1-now) * 50)+"%";
                    //3. increase opacity of previous_fs to 1 as it moves in
                    opacity = 1 - now;
                    current_fs.css({'left': left});
                    previous_fs.css({'transform': 'scale('+scale+')', 'opacity': opacity, 'position': 'relative'});
                },
                duration: 800,
                complete: function(){
                    current_fs.hide();
                    animating = false;
                },
                //this comes from the custom easing plugin
                easing: 'easeInOutBack'
            });
            if($(this).hasClass('hide_total')) {
                $('#msform').parent().removeClass('offset-md-2');
                $('#msform').parent().addClass('offset-md-3');
                $('#msform').parent().next().css("display", "none")
            }
        });

        $('.addStar').click(function(ths,sno) {
            for(var i = 1; i <= 5; i++) {
                var cur = document.getElementById("star" + i);
                cur.className = "fa fa-star";
            }
            for(var i = 1; i <= sno; i++) {
                var cur = document.getElementById("star" + i)
                if(cur.className == "fa fa-star") {
                    cur.className = "fa fa-star checked"
                }
            }
            $(this).parent().next().val(sno);
        });


    });
});
