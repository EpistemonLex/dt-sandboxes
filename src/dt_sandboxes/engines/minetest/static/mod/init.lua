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
    local data = minetest.write_json({
        sandbox_type = "minetest",
        event_name = event_name,
        payload = payload,
        level = "info",
        timestamp = os.date("!%Y-%m-%dT%H:%M:%SZ")
    })

    http.fetch({
        url = HARVESTER_URL,
        method = "POST",
        data = data,
        timeout = 2,
        post_data = data, -- compatibility
    }, function(res)
        if not res.succeeded then
            minetest.log("warning", "[Ed-OS] Telemetry broadcast failed: " .. tostring(res.code))
        end
    end)
end

-- 1. Observe Movement (Gravity Trigger)
local player_states = {}

minetest.register_globalstep(function(dtime)
    for _, player in ipairs(minetest.get_connected_players()) do
        local name = player:get_player_name()
        local pos = player:get_pos()
        local vel = player:get_velocity()
        
        if vel.y < -10 then -- Fast falling
            if not player_states[name] or player_states[name].state ~= "falling" then
                player_states[name] = { state = "falling", start_pos = pos }
                broadcast("player_falling", { name = name, velocity_y = vel.y, pos = pos })
            end
        elseif vel.y >= 0 and player_states[name] and player_states[name].state == "falling" then
            -- Landed
            local fall_dist = player_states[name].start_pos.y - pos.y
            broadcast("player_landed", { name = name, fall_distance = fall_dist, pos = pos })
            player_states[name] = nil
        end
    end
end)

-- 2. Observe Block Placement
minetest.register_on_placenode(function(pos, newnode, placer, oldnode, itemstack, pointed_thing)
    if placer and placer:is_player() then
        broadcast("node_placed", {
            name = placer:get_player_name(),
            node = newnode.name,
            pos = pos
        })
    end
end)

minetest.log("action", "[Ed-OS] Harvester Mod loaded and observing world.")
