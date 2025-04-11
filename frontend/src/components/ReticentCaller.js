function cancellableUpdate(fetchFunction, updateFunction, timeout) {
    var cancelled = false;
    const wait = new Promise(resolve => { setTimeout(resolve, timeout) });
    const performFetch = wait.then(() => {
        if (!cancelled) { return fetchFunction() }
    });
    const performUpdate = performFetch.then((fetchResult) => {
        if (!cancelled) {
            updateFunction(fetchResult);
        }
    })
    performUpdate.cancel = () => {
        cancelled = true;
    }
    return performUpdate;
}

export default class ReticentUpdater {
    constructor(pauseBeforeCallingMilliSeconds, fetchFunction, updateFunction) {
        this.pauseBeforeCallingMilliSeconds = pauseBeforeCallingMilliSeconds;
        this.updatePromise = null;
        this.fetchFunction = fetchFunction;
        this.updateFunction = updateFunction;
    }

    triggerUpdate(fetchArg) {
        if (this.updatePromise) {
            this.updatePromise.cancel()
        }
        this.updatePromise = cancellableUpdate(() => this.fetchFunction(fetchArg), this.updateFunction, this.pauseBeforeCallingMilliSeconds);
    }
}