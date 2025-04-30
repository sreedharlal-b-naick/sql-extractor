-module(employee_dal).

-include("log.hrl").

-export([
    add_employee/5
]).

add_employee(ShopId, Phone, Name, Role, Permissions) ->
    ?Info("Adding employee phone= ~p with name= ~s and role: ~s", [Phone, Name, Role]),
    Result = martzo_pg_dal:run_query(
        "INSERT INTO employee(phone, shop_id, name, role, status, permissions) VALUES ($1, $2, $3, $4, 'available', $5)",
        [Phone, ShopId, Name, Role, Permissions]
    ),
    case Result of
        1 -> ok;
        _ -> {error, <<"Error adding employee">>}
    end.