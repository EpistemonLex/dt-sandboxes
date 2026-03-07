-- Deepthought Ed-OS: Minetest Harvester Mod
-- 
-- Intercepts world events and broadcasts them to the Backpack daemon.

local HARVESTER_URL = "http://localhost:8000/telemetry/minetest"
local http = minetest.request_http_api()

if not http then
    minetest.log("error", "[Ed-OS] HTTP API not found! Add 'edos_harvester' to secure.http_mods.")
    return
end

local function broadcast(event_name, payload)
    local data = {
        sandbox_type = "minetest",
        event_name = event_name,
        payload = payload,
        level = "info",
        timestamp = os.date("!%Y-%m-%dT%H:%M:%SZ")
    }
    
    http.fetch({
        url = HARVESTER_URL,
        method = "POST",
        data = minetest.write_json(data),
        timeout = 2,
    }, function(res)
        if not res.succeeded then
            minetest.log("warning", "[Ed-OS] Failed to send telemetry: " .. event_name)
        end
    end)
end

-- 1. Hook into Block Events
minetest.register_on_placenode(function(pos, newnode, placer, oldnode, itemstack, pointed_thing)
    broadcast("block_event", {
        pos = pos,
        block_name = newnode.name,
        action = "place"
    })
end)

minetest.register_on_dignode(function(pos, oldnode, digger)
    broadcast("block_event", {
        pos = pos,
        block_name = oldnode.name,
        action = "dig"
    })
end)

-- 2. Periodic Player Sync (Spatial Reasoning)
local timer = 0
minetest.register_globalstep(function(dtime)
    timer = timer + dtime
    if timer >= 5 then
        timer = 0
        for _, player in ipairs(minetest.get_connected_players()) do
            broadcast("state_update", {
                player_pos = player:get_pos(),
                player_hp = player:get_hp(),
                inventory_count = player:get_inventory():get_size("main"),
                active_mod_version = "1.0.0"
            })
        end
    end
end)

minetest.log("action", "[Ed-OS] Minetest Harvester Loaded.")
