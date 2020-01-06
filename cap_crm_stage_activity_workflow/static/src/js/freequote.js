odoo.define('cap_crm_stage_activity_workflow.freequote', function (require) {
    "use strict";
    $(document).ready(function () {
        $(".col-form-label").click(function () {
            var $title = $(this).find(".title");
            if (!$title.length) {
                if($(this).attr("title")){
                    $(this).append('<span class="title"><br/>' + $(this).attr("title") + '</span>');
                }
            } else {
                $title.remove();
            }
        });
    });
});
