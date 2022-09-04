export class AppConfig {
  protected static base = 'http://127.0.0.1:5050'

  static get endpoint(): string {
    return `${AppConfig.base}/api`
  }

  static get assetEndpoint(): string {
    return `${AppConfig.base}/`
  }
}
