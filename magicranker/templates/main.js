YAHOO.util.Event.onDOMReady(
    function() {
        var Dom = YAHOO.util.Dom,
            Event = YAHOO.util.Event,
            Button = YAHOO.widget.Button,
            ButtonGroup = YAHOO.widget.ButtonGroup,
            Tooltip = YAHOO.widget.Tooltip;
            // Setup tool tips
            var myTooltip = new Tooltip("roe_title_tt", {
                context: "roe_title",
                text: "Return on Equity"
            });
            var myTooltip = new Tooltip("pe_title_tt", {
                context: "pe_title",
                text: "Price / Earnings" 
            });
            var myTooltip = new Tooltip("mcap_title_tt", {
                context: "mcap_title",
                text: "Market Cap" 
            });
            var myTooltip = new Tooltip("debt_title_tt", {
                context: "debt_title",
                text: "Debt" 
            });
            // define a submit Button object
            var main_submit = new Button("main_submit");
            var rank_roe = new Button("roe_check", { 
                type:"checkbox", 
                value:"Yes", 
                checked:{% if rank_roe %}true{% else %}false{% endif %} 
            });
            var debt_check = new Button("debt_check", { 
                type:"checkbox", 
                value:"Yes", 
                checked:{% if debt_check %}true{% else %}false{% endif %} });
            var filt_market_cap = new Button("filt_market_cap", { 
                type:"checkbox", 
                value:"Yes", 
                checked:{% if filt_market_cap %}true{% else %}false{% endif %} 
            });
            var rank_pe = new Button("rank_pe", { 
                type:"checkbox", 
                value:"Yes", 
                checked:{% if rank_pe %}true{% else %}false{% endif %}
            });
            //var roe_group = new ButtonGroup("roe_group", {disabled: true});
            //var debt_group = new ButtonGroup("debt_group", {disabled: true});
            //var market_cap_group = new ButtonGroup("market_cap_group", {disabled: true});
            // When Radio Buttons are checked, set button on
            var roe_options_list = ["roe_options1", "roe_options2", "roe_options3"];
            Event.on(
                roe_options_list, 
                "click", 
                function() {
                    rank_roe.set("checked", true);
                }
            );
            var pe_options_list = ["pe_options"];
            Event.on(
                pe_options_list, 
                "click", 
                function() {
                    pe_check.set("checked", true);
                }
            );
            var market_cap_options_list = ["market_cap_options1", 
                                           "market_cap_options2"];
            Event.on(
                market_cap_options_list, 
                "click", 
                function() {
                    filt_market_cap.set("checked", true);
                }
            );
            var debt_options_list = ["debt_options1", 
                                     "debt_options2", 
                                     "debt_options3", 
                                     "debt_options4", 
                                     "debt_options5"];
            Event.on(
                debt_options_list, 
                "click", 
                function() {
                    debt_check.set("checked", true);
                }
            );
            // Function sets the roe_group check box to previous value
            //var roe_view = function (e) {
            //	roe_group.set("disabled", e.prevValue);
            //};
            // Function sets the roe_group check box to previous value
            //var market_cap_view = function (e) {
            //	market_cap_group.set("disabled", e.prevValue);
            //};
            // Function sets the roe_group check box to previous value
            //var debt_view = function (e) {
            //	debt_group.set("disabled", e.prevValue);
            //};
            
            // Run the roe_view fucntion when checked value of the rank_roe is changed
            //rank_roe.on("checkedChange", roe_view);								
            
            
            // Run the roe_view fucntion when checked value of the rank_roe is changed
            //filt_market_cap.on("checkedChange", market_cap_view);
            
            // Run the roe_view fucntion when checked value of the rank_roe is changed
            //debt_check.on("checkedChange", debt_view);
    });
