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
        <p><a href="/record">灌水啦</a></p>
        <p><a href="/view">查水表</a></p>
        <p><a href="/defaults">查默表</a></p>
        <p><a href="/currencies">查币表</a></p>
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
            <td><input class="TextInput" type=text name=ware{{i}} size=25 value='{{row.ware}}'></td>
            
            <td> &nbsp; 金额</td>
            <td><select class="Select" name=currency{{i}}>
            % for c in AllCurrencies :
                <option value={{c.members['curid']}} {{'selected' if c.members['curid']==row.currency else ''}}>{{!c.members['html']}}
            % end
                </select>
                <input class="TextInput" type=text name=cost{{i}} size=10 value='{{row.cost}}'>
            </td>
            
            <td> &nbsp; 备注</td>
            <td><input class="TextInput" type=text name=remark{{i}} size=30 value='{{row.remark}}'></td>
            
            <td> &nbsp; 日期</td>
            <td><input class="TextInput" type=text name=year{{i}} size=4 value='{{row.year}}'> -
                <input class="TextInput" type=text name=month{{i}} size=2 value='{{row.month}}'> -
                <input class="TextInput" type=text name=day{{i}} size=2 value='{{row.day}}'>
            </td>
        </tr>
    % end
        </table>
        <input class="Button" type=submit value='提交'>
    </form>
% end


% if operation == 'VIEW' :
    <form method=post action="/view">
        <table style="margin-top:10px; margin-bottom: 10px; border: 0px solid #3399FF;">
        <tr>
            <td width=100><font size=3 color=#3399FF>选择年月</font></td>
            <td width=180><select class="Select" name=year>
            % for y in AllYears :
                <option {{'selected' if y==year else ''}}>{{y}}
            % end
                </select>
                <select class="Select" name=month>
            % for m in [ '%02d' % mo for mo in range(1,13) ] :
                <option {{'selected' if m==month else ''}}>{{m}}
            % end
                </select>
            </td>
            <td width=150><input class="Button" type=checkbox name='daily'> Daily View</td>
            <td width=120><input class="Button" type=submit value='查询'></td>
        </tr>
        </table>
    </form>
    
    <div style="border-bottom: 1px solid #3399FF; width: 550px;"></div>
    
    <table class="table_border" style="margin-top:20px; margin-bottom: 20px;">
        <tr align=center>
            <td width=100>日期</td>
        % if not daily :
            <td width=200>商品</td>
        % end
            <td width=150>金额</td>
        % if not daily :
            <td width=200>备忘</td>
            <td width=100>操作</td>
        % end
        </tr>
        % if not daily :
            % for row in IncomeRows :
            <tr align=center>
                <td><font color=green>Income</font></td>
                <td>-</td>
                <td><font color=green>{{!row.cost}}</font></td>
                <td>-</td>
                <td>-</td>
            </tr>
            % end
            <tr><td colspan={{5 if not daily else 2}}></td></tr>
        % end
        % for row in ExpensesRows :
            <tr align=center>
                <td><font color=green>Expenses</font></td>
            % if not daily :
                <td>-</td>
            % end
                <td><font color=green>{{!row.cost}}</font></td>
            % if not daily :
                <td>-</td>
                <td>-</td>
            % end
            </tr>
        % end
        % if not daily :
        <tr><td colspan={{5 if not daily else 2}}></td></tr>
            % for row in BalanceRows :
            <tr align=center>
                <td><font color=green>Balance</font></td>
                <td>-</td>
                <td><font color=green>{{!row.cost}}</font></td>
                <td>-</td>
                <td>-</td>
            </tr>
            % end
        % end
        <tr><td colspan={{5 if not daily else 2}}></td></tr>
    % for row in TallyRows :
        <tr align=center>
            <td>{{row.date}}</td>
        % if not daily :
            <td>{{row.ware}}</td>
        % end
            <td>{{!row.cost}}</td>
        % if not daily :
            <td>{{row.remark}}</td>
            <td>
                <form method=post action="/view_delete">
                    <input type=hidden name=date value='{{ "%s-%s" % (year,month) }}'>
                    <input type=hidden name=delete value='{{row.talid}}'>
                    <input class="TableButton" type=submit value='删除'>
                </form>
            </td>
        % end
        </tr>
    % end
    </table>
% end


% if operation == 'SETTINGS' :
    <p><font size=3 color=#3399FF>修改默认货币</font></p>
    <form method=post action="/settings/default_currency">
        <table style="margin-top:10px; margin-bottom: 20px; border: 0px solid #3399FF;">
        <tr>
            <td width=100><select class="Select" name=currency>
            % for c in AllCurrencies :
                <option value={{c.members['curid']}} {{'selected' if c.members['curid']==currency else ''}}>{{!c.members['html']}}
            % end
                </select>
            </td>
            <td width=50></td>
            <td><input class="Button" type=submit value='确定'></td>
        </tr>
        </table>
    </form>
    
    <div style="border-bottom: 1px solid #3399FF; width: 300px;"></div>
    
    <p><font size=3 color=#3399FF>修改默认每次输入的记录数</font></p>
    <form method=post action="/settings/num_of_rows">
        <table style="margin-top:10px; margin-bottom: 20px; border: 0px solid #3399FF;">
        <tr>
            <td width=100><select class="Select" name=num_of_rows>
            % for i in range( 1, 11 ) :
                <option {{'selected' if i==num_of_rows else ''}}>{{i}}
            % end
                </select>
            </td>
            <td width=50></td>
            <td><input class="Button" type=submit value='确定'></td>
        </tr>
        </table>
    </form>
    
    <div style="border-bottom: 1px solid #3399FF; width: 300px;"></div>
    
    <p><font size=3 color=#3399FF>添加新货币</font></p>
    <form method=post action="/settings/add_currency">
        <table style="margin-top:10px; margin-bottom: 20px; border: 0px solid #3399FF;">
        <tr>
            <td colspan=4><font color=red>{{CurrencyToAdd.msg}}</font></td>
        </tr>
        <tr>
            <td width=110>货币名称</td>
            <td width=120>符号</td>
            <td width=130>HTML符号</td>
            <td width=140>UNICODE符号</td>
        </tr>
        <tr>
            <td><input class="TextInput" type=text name=name size=8 value='{{CurrencyToAdd.members['name']}}'></td>
            <td><input class="TextInput" type=text name=symbol size=10 value='{{CurrencyToAdd.members['symbol']}}'></td>
            <td><input class="TextInput" type=text name=html size=12 value='{{CurrencyToAdd.members['html']}}'></td>
            <td><input class="TextInput" type=text name=unicode size=14 value='{{CurrencyToAdd.members['uni']}}'></td>
        </tr>
        <tr>
            <td colspan=2>英文全称</td>
            <td colspan=2 rowspan=2 valign=bottom><input class="Button" type=submit value='确定'></td>
        </tr>
        <tr>
            <td colspan=2><input class="TextInput" type=text name=description size=28 value='{{CurrencyToAdd.members['desc']}}'></td>
        </tr>
        </table>
    </form>
    
    <div style="border-bottom: 1px solid #3399FF; width: 300px;"></div>
    
    <p><font size=3 color=#3399FF>删除货币</font></p>
    <form method=post action="/settings/delete_currency">
        <table style="margin-top:10px; margin-bottom: 20px; border: 0px solid #3399FF;">
        <tr>
            <td width=100><select class="Select" name=currency>
                <option value=0> (.^__^.)
            % for c in AllCurrencies :
                <option value={{c.members['curid']}}>{{!c.members['html']}}
            % end
                </select>
            </td>
            <td width=50></td>
            <td><input class="Button" type=submit value='确定'></td>
        </tr>
        </table>
    </form>
% end


% if operation == 'DEFAULTS' :
    <p><font size=3 color=#3399FF>默认值表</font></p>
    <div style="border-bottom: 1px solid #3399FF; width: 300px;"></div>
    
    <table class="table_border" style="margin-top:20px; margin-bottom: 20px;">
        <tr align=center>
            <td width=200>KEY</td>
            <td width=150>VALUE</td>
        </tr>
    % for d in default_values :
        <tr align=center>
            <td>{{d.key}}</td>
            <td>{{d.value}}</td>
        </tr>
    % end
    </table>
% end


% if operation == 'CURRENCIES' :
    <p><font size=3 color=#3399FF>货币表</font></p>
    <div style="border-bottom: 1px solid #3399FF; width: 300px;"></div>
    
    <table class="table_border" style="margin-top:20px; margin-bottom: 20px;">
        <tr align=center>
            <td width=50>ID</td>
            <td width=100>货币名称</td>
            <td width=100>货币符号</td>
            <td width=100>HTML</td>
            <td width=100>UNICODE</td>
            <td width=200>货币全称</td>
        </tr>
    % for c in currencies :
        <tr align=center>
            <td>{{c.members['curid']}}</td>
            <td>{{c.members['name']}}</td>
            <td>{{c.members['symbol']}}</td>
            <td>{{c.members['html']}}</td>
            <td>{{c.members['uni']}}</td>
            <td>{{c.members['desc']}}</td>
        </tr>
    % end
    </table>
% end

</div>
</div>
</body>
