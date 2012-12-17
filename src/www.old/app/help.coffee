
# Randomly add a data point every 500ms
random = new TimeSeries()
setInterval (() ->
    random.append(new Date().getTime(), Math.random() * 10000)
    #log '-+-+-+-'
), 200
setInterval (() ->
    random.append(new Date().getTime(), Math.random() * 10000)
    #log '-+-+-+-'
), 200

createTimeline = () ->
    chart = new SmoothieChart()
    chart.addTimeSeries(random, { strokeStyle: 'rgba(0, 255, 0, 1)', fillStyle: 'rgba(0, 255, 0, 0.2)', lineWidth: 3 })
    chart.streamTo(document.getElementById("chart"), 200)


