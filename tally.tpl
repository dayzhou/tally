<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<!-- <link href="tally.css" rel=stylesheet type=text/css> -->
<title>Tally</title>

<style type="text/css">
% include( 'tally.css' )
</style>

</head>
<body>

<div class="left">
    <div class="left_box">
        <p><a href="/record">记账啦</a></p>
        <p><a href="/view">查水表</a></p>
        <p><a href="/settings">设置</a></p>
    </div>
</div>

<div class="right">
<div class="right_box">

% if operation == 'RECORD' :
    <p><font size=3 color=#3399FF>收入或支出</font></p>
    <div style="border-bottom: 1px solid #3399FF; width: 300px;"></div>
    
    <form method=post action="/record">
        <table cellspacing=5 style="margin-top:10px; margin-bottom: 10px; border: 0px solid #3399FF;">
    % for i,row in enumerate( InputRows ) :
        <tr>
            <td></td>
            <td><font color=red>{{row.msg['ware']}}</font></td>
            
            <td></td>
            <td><font color=red>{{row.msg['cost']}}</font></td>
            
            <td></td>
            <td><font color=red>{{row.msg['remark']}}</font></td>
            
            <td></td>
            <td><font color=red>{{row.msg['date']}}</font></td>
        </tr>
        <tr>
            <td>商品</td>
            <td><input type=text name=ware{{i}} size=25 value='{{row.ware}}'></td>
            
            <td> &nbsp; 金额</td>
            <td><select name=currency{{i}}>
            % for c in AllCurrencies :
                <option value={{c.members['curid']}} {{'selected' if c.members['curid']==row.currency else ''}}>{{!c.members['html']}}
            % end
                </select>
                <input type=text name=cost{{i}} size=10 value='{{row.cost}}'>
            </td>
            
            <td> &nbsp; 备注</td>
            <td><input type=text name=remark{{i}} size=30 value='{{row.remark}}'></td>
            
        % year, month, day = row.date.split('-')
            <td> &nbsp; 日期</td>
            <td><input type=text name=year{{i}} size=4 value='{{year}}'> -
                <input type=text name=month{{i}} size=2 value='{{month}}'> -
                <input type=text name=day{{i}} size=2 value='{{day}}'>
            </td>
        </tr>
    % end
        </table>
        <input class="LoginButton" type=submit value='提交'>
    </form>
% end


% if operation == 'VIEW' :
    <form method=post action="/view">
        <table style="margin-top:10px; margin-bottom: 10px; border: 0px solid #3399FF;">
        <tr>
            <td width=100><font size=3 color=#3399FF>选择年月</font></td>
            <td width=200><select name=year>
            % for y in AllYears :
                <option {{'selected' if y==year else ''}}>{{y}}
            % end
                </select>
                <select name=month>
            % for m in [ '%02d' % mo for mo in range(1,13) ] :
                <option {{'selected' if m==month else ''}}>{{m}}
            % end
                </select>
            </td>
            <td><input class="LoginButton" type=submit value='查询'></td>
        </tr>
        </table>
    </form>
    
    <div style="border-bottom: 1px solid #3399FF; width: 400px;"></div>
    
    <table class="table_border" style="margin-top:20px;">
        <tr align=center>
            <td width=100>日期</td>
            <td width=200>商品</td>
            <td width=120>金额</td>
            <td width=200>备忘</td>
        </tr>
    % for row in TallyRows :
        <tr align=center>
            <td width=100>{{row.date}}</td>
            <td width=200>{{row.ware}}</td>
            <td width=120>{{!row.cost}}</td>
            <td width=200>{{row.remark}}</td>
        </tr>
    % end
        <tr><td colspan=4></td></tr>
        % for row in IncomeRows :
            <tr align=center>
            <td width=100><font color=green>Income</font></td>
            <td width=200>-</td>
            <td width=120><font color=green>{{!row.cost}}</font></td>
            <td width=200>-</td>
            </tr>
        % end
        <tr><td colspan=4></td></tr>
        % for row in ExpensesRows :
            <tr align=center>
            <td width=100><font color=green>Expenses</font></td>
            <td width=200>-</td>
            <td width=120><font color=green>{{!row.cost}}</font></td>
            <td width=200>-</td>
            </tr>
        % end
        <tr><td colspan=4></td></tr>
        % for row in BalanceRows :
            <tr align=center>
            <td width=100><font color=green>Balance</font></td>
            <td width=200>-</td>
            <td width=120><font color=green>{{!row.cost}}</font></td>
            <td width=200>-</td>
            </tr>
        % end
    </table>
% end


% if operation == 'SETTINGS' :
    <p><font size=3 color=#3399FF>修改默认货币</font></p>
    <form method=post action="/settings/default_currency">
        <table style="margin-top:10px; margin-bottom: 20px; border: 0px solid #3399FF;">
        <tr>
            <td width=100><select name=currency>
            % for c in AllCurrencies :
                <option value={{c.members['curid']}} {{'selected' if c.members['curid']==currency else ''}}>{{!c.members['html']}}
            % end
                </select>
            </td>
            <td width=50></td>
            <td><input class="LoginButton" type=submit value='确定'></td>
        </tr>
        </table>
    </form>
    
    <div style="border-bottom: 1px solid #3399FF; width: 300px;"></div>
    
    <p><font size=3 color=#3399FF>修改默认每次输入的记录数</font></p>
    <form method=post action="/settings/num_of_rows">
        <table style="margin-top:10px; margin-bottom: 20px; border: 0px solid #3399FF;">
        <tr>
            <td width=100><select name=num_of_rows>
            % for i in range( 1, 11 ) :
                <option {{'selected' if i==num_of_rows else ''}}>{{i}}
            % end
                </select>
            </td>
            <td width=50></td>
            <td><input class="LoginButton" type=submit value='确定'></td>
        </tr>
        </table>
    </form>
    
    <div style="border-bottom: 1px solid #3399FF; width: 300px;"></div>
    
    <p><font size=3 color=#3399FF>添加新货币</font></p>
    <form method=post action="/settings/add_currency">
        <table style="margin-top:10px; margin-bottom: 20px; border: 0px solid #3399FF;">
        <tr>
            <td colspan=4><font color=red>{{'' if CurrencyToAdd.get_check_stat() else u'所有货币属性不可为空，且不可与已有货币重复'}}</font></td>
        </tr>
        <tr>
            <td width=110>货币名称</td>
            <td width=120>符号</td>
            <td width=130>HTML符号</td>
            <td width=140>UNICODE符号</td>
        </tr>
        <tr>
            <td><input type=text name=name size=8 value='{{CurrencyToAdd.members['name']}}'></td>
            <td><input type=text name=symbol size=10 value='{{CurrencyToAdd.members['symbol']}}'></td>
            <td><input type=text name=html size=12 value='{{CurrencyToAdd.members['html']}}'></td>
            <td><input type=text name=unicode size=14 value='{{CurrencyToAdd.members['uni']}}'></td>
        </tr>
        <tr>
            <td colspan=2>英文全称</td>
            <td colspan=2 rowspan=2 valign=bottom><input class="LoginButton" type=submit value='确定'></td>
        </tr>
        <tr>
            <td colspan=2><input type=text name=description size=28 value='{{CurrencyToAdd.members['desc']}}'></td>
        </tr>
        </table>
    </form>
    
    <div style="border-bottom: 1px solid #3399FF; width: 300px;"></div>
    
    <p><font size=3 color=#3399FF>删除货币</font></p>
    <form method=post action="/settings/delete_currency">
        <table style="margin-top:10px; margin-bottom: 20px; border: 0px solid #3399FF;">
        <tr>
            <td width=100><select name=currency>
                <option value=0> (.^__^.)
            % for c in AllCurrencies :
                <option value={{c.members['curid']}}>{{!c.members['html']}}
            % end
                </select>
            </td>
            <td width=50></td>
            <td><input class="LoginButton" type=submit value='确定'></td>
        </tr>
        </table>
    </form>
% end

</div>
</div>
</body>