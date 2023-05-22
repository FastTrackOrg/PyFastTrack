import sentry_sdk
sentry_sdk.init(
    dsn="https://5dff536b23ee400db3e2f247edf1d711@o4505228290031616.ingest.sentry.io/4505228343967744",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)
