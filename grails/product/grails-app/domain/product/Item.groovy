package product

class Item {
    
    String name
    String description
    String manufacturer
    Date receiptDate
    double cost
    double price

    def list() {
        log.info "test..."
    }

    static constraints = {
    }
}
