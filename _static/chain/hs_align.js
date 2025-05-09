        /**
 * Experimental Highcharts plugin to implement chart.alignThreshold option. This primary axis
 * will be computed first, then all following axes will be aligned to the threshold.
 * Author: Torstein Hønsi
 * Last revision: 2016-11-02
 */
(function (H)
{
    const Axis = H.Axis;
    const wrap = H.wrap;

    wrap(Axis.prototype, 'adjustTickAmount', function (proceed)
    {
        const chart = this.chart;
        const primaryAxis = chart[this.coll][0];
        let primaryThreshold;
        let primaryIndex;
        let index;
        let newTickPos;
        let threshold;

        // Find the index and return boolean result
        function isAligned(axis)
        {
            index = axis.tickPositions.indexOf(threshold); // used in while-loop
            return axis.tickPositions.length === axis.tickAmount && index === primaryIndex;
        }

        if (chart.options.chart.alignThresholds && this !== primaryAxis)
        {
            primaryThreshold = (primaryAxis.series[0] && primaryAxis.series[0].options.threshold) || 0;
            threshold = (this.series[0] && this.series[0].options.threshold) || 0;

            primaryIndex = primaryAxis.tickPositions && primaryAxis.tickPositions.indexOf(
                primaryThreshold
            );

            if (!this.tickPositions || !this.tickPositions.length || !this.tickAmount)
            {
                proceed.call(this);
                return;
            }

           
            if (primaryIndex === 0)
            {
                while (!isAligned(this))
                {
                    newTickPos = primaryAxis.tickPositions[0] - primaryAxis.tickInterval;
                    primaryAxis.tickPositions.unshift(newTickPos);
                    primaryAxis.min = newTickPos;
                    primaryAxis.tickAmount++;
                    this.tickAmount++;
                    primaryIndex = primaryAxis.tickPositions.indexOf(primaryThreshold);
                    proceed.call(this);
                }
            }
            else if (primaryIndex === primaryAxis.tickPositions.length - 1)
            {
                while (!isAligned(this))
                {
                    newTickPos = primaryAxis.tickPositions[this.tickPositions.length - 1] + primaryAxis.tickInterval;
                    primaryAxis.tickPositions.push(newTickPos);
                    primaryAxis.max = newTickPos;
                    primaryAxis.tickAmount++;
                    this.tickAmount++;
                    primaryIndex = primaryAxis.tickPositions.indexOf(primaryThreshold);
                    proceed.call(this);
                }
            }
            
            if (primaryIndex > 0 && primaryIndex < primaryAxis.tickPositions.length - 1)
            {
                // Add tick positions to the top or bottom in order to align the threshold
                // to the primary axis threshold
                while (!isAligned(this))
                {
                    if (index < primaryIndex)
                    {
                        newTickPos = this.tickPositions[0] - this.tickInterval;
                        this.tickPositions.unshift(newTickPos);
                        this.min = newTickPos;
                        proceed.call(this);
                        continue;
                    }
                    
                    newTickPos = this.tickPositions[this.tickPositions.length - 1] + this.tickInterval;
                    this.tickPositions.push(newTickPos);
                    this.max = newTickPos;
                    proceed.call(this);
                }
            }

            return;
        }

        proceed.call(this);
    });
}(Highcharts));