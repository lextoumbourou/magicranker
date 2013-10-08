function click_option(field_name)
{
    $("#" + field_name + "_set_btn").on('click', '', function() {
        var rank_input = $("input[name='" + field_name + "']");
        if (rank_input.val() == "") {
            rank_input.val("1");
        }
        else {
            rank_input.val("");
        }
    });
}

function limit_click()
{
    $(".limit_btn").on('click', '', function() {
        var rank_input = $("input[name='limit']").val($(this).attr('value'));
    });
}

function change_parent(elements, parent_elem) {
    for (var i = 0; i < elements.length; i++)
    {
        $('#' + elements[i]).on('click', '', function() {
            var rank_input = $("input[name='" + parent_elem + "']");
            rank_input.val("1");
            $('#' + parent_elem + '_set_btn').addClass('active');
        });
    }
}

click_option('rank_roe');
click_option('rank_pe');
click_option('filter_market_cap');
click_option('filter_debt');
limit_click();
change_parent(['rank_roe_max', 'rank_roe_avg'], 'rank_roe');
change_parent(['rank_pe_min'], 'rank_pe');
change_parent(['filter_market_cap_min'], 'filter_market_cap');
change_parent(['filter_debt_max'], 'filter_debt');
