import java.util.*;
import java.util.concurrent.*;

// === Stock Class ===
class Stock {
    private final String symbol;
    private double price;
    private int volume;

    public Stock(String symbol, double price) {
        this.symbol = symbol;
        this.price = price;
        this.volume = 0;
    }

    public synchronized double getPrice() {
        return price;
    }

    public synchronized void updatePrice() {
        price += (Math.random() - 0.5) * 10;
        if (price < 1) price = 1;
    }

    public String getSymbol() {
        return symbol;
    }

    public synchronized void addVolume(int quantity) {
        volume += quantity;
    }

    public synchronized int getVolume() {
        return volume;
    }

    public String toString() {
        return symbol + " @ ₹" + String.format("%.2f", price);
    }
}

// === Abstract User Class ===
abstract class User {
    protected String name;
    protected Map<String, Integer> portfolio = new ConcurrentHashMap<>();

    public User(String name) {
        this.name = name;
    }

    public abstract double getTradeFee();

    public void buyStock(Stock stock, int quantity) {
        double totalCost = stock.getPrice() * quantity + getTradeFee();
        System.out.println(name + " bought " + quantity + " of " + stock.getSymbol() + " for ₹" + String.format("%.2f", totalCost));
        portfolio.merge(stock.getSymbol(), quantity, Integer::sum);
        stock.addVolume(quantity);
    }

    public void sellStock(Stock stock, int quantity) {
        int owned = portfolio.getOrDefault(stock.getSymbol(), 0);
        if (owned < quantity) {
            System.out.println(name + " does not have enough shares of " + stock.getSymbol());
            return;
        }
        double totalEarned = stock.getPrice() * quantity - getTradeFee();
        System.out.println(name + " sold " + quantity + " of " + stock.getSymbol() + " for ₹" + String.format("%.2f", totalEarned));
        portfolio.put(stock.getSymbol(), owned - quantity);
        stock.addVolume(quantity);
    }
}

// === User Types ===
class RetailInvestor extends User {
    public RetailInvestor(String name) {
        super(name);
    }

    public double getTradeFee() {
        return 20.0; // Flat fee
    }
}

class InstitutionalInvestor extends User {
    public InstitutionalInvestor(String name) {
        super(name);
    }

    public double getTradeFee() {
        return 5.0; // Lower fee
    }
}

// === Trading Platform ===
class TradingPlatform {
    private Map<String, Stock> stockMarket = new ConcurrentHashMap<>();
    private ExecutorService executor = Executors.newCachedThreadPool();

    public TradingPlatform() {
        stockMarket.put("TCS", new Stock("TCS", 3200));
        stockMarket.put("INFY", new Stock("INFY", 1400));
        stockMarket.put("RELIANCE", new Stock("RELIANCE", 2400));
        stockMarket.put("HDFC", new Stock("HDFC", 1600));
        stockMarket.put("SBIN", new Stock("SBIN", 600));
    }

    public void startPriceUpdates() {
        Runnable updater = () -> {
            while (!Thread.currentThread().isInterrupted()) {
                for (Stock stock : stockMarket.values()) {
                    stock.updatePrice();
                }
                try {
                    Thread.sleep(2000); // update every 2 seconds
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        };
        executor.submit(updater);
    }

    public void simulateUserTrades(User user) {
        Runnable trader = () -> {
            Random random = new Random();
            List<Stock> stocks = new ArrayList<>(stockMarket.values());

            for (int i = 0; i < 5; i++) {
                Stock stock = stocks.get(random.nextInt(stocks.size()));
                int quantity = 1 + random.nextInt(5);
                if (random.nextBoolean()) {
                    user.buyStock(stock, quantity);
                } else {
                    user.sellStock(stock, quantity);
                }
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    break;
                }
            }
        };
        executor.submit(trader);
    }

    public void displayTopTradedStocks() {
        System.out.println("\nTop 5 Stocks by Volume:");
        stockMarket.values().stream()
            .sorted((a, b) -> b.getVolume() - a.getVolume())
            .limit(5)
            .forEach(s -> System.out.println(s.getSymbol() + " | Volume: " + s.getVolume()));
    }

    public void shutdown() {
        executor.shutdownNow();
    }
}

// === Main Class ===
public class Main {
    public static void main(String[] args) throws InterruptedException {
        TradingPlatform platform = new TradingPlatform();
        User user1 = new RetailInvestor("Amit");
        User user2 = new InstitutionalInvestor("LIC");

        platform.startPriceUpdates();
        platform.simulateUserTrades(user1);
        platform.simulateUserTrades(user2);

        Thread.sleep(12000); // Run for 12 seconds

        platform.displayTopTradedStocks();
        platform.shutdown();
    }
}
