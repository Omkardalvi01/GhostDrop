local keys = redis.call('KEYS', ARGV[1])
local results = {}
for i, key in ipairs(keys) do
    local ttl = redis.call('TTL', key)
    if ttl > 0 then
        table.insert(results, {key, ttl})
    end
end

table.sort(results, function(a, b) return a[2] < b[2] end)
return results