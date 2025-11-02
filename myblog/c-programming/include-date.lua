function Meta(meta)
  -- 每次渲染时把 date 设置为系统当前日期
  meta.date = os.date("%Y-%m-%d")
  return meta
end
