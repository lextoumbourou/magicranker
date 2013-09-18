function click_option(field_name)
{
    $("#" + field_name + "_set_btn").on('click', '', function() {
        if ($(this).hasClass('btn-primary'))
        {
            $(this).removeClass('btn-primary');
        }
        else
        {
            $(this).addClass('btn-primary');
        }
        var rank_input = $("input[name='" + field_name + "']");
        if (rank_input.val() == "1")
        {
            rank_input.val("0");
        }
        else
        {
            rank_input.val("1");
        }
    });
}

function limit_click()
{
    $(".limit_btn").on('click', '', function() {
        $(".limit_btn").removeClass('btn-primary');
        $(this).addClass('btn-primary');
        var rank_input = $("input[name='limit']").val($(this).attr('value'));
    });
}

click_option('rank_roe');
click_option('rank_pe');
click_option('filter_market_cap');
click_option('filter_debt');
limit_click();
