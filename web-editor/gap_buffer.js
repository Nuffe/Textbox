
class GapBuffer {
    constructor(size) {
        this.size = size;
        this.gapSize = 10;
        this.buffer = new Array(this.size).fill(null);
        this.gapStart = 0;
        this.gapEnd = this.gapSize;
    }

    // increases the size of the gap
    grow(amount, position) {
        this.buffer.splice(position, 0, ...new Array(amount).fill(null));
        this.size += amount;
        this.gapEnd += amount;
        this.gapSize += amount;
    }

    right(position) {
        while (position > this.gapStart) {
            if (this.gapEnd >= this.buffer.length) break;
            this.buffer[this.gapStart] = this.buffer[this.gapEnd];
            this.buffer[this.gapEnd] = null;
            this.gapStart += 1;
            this.gapEnd += 1;
        }
    }

    left(position) {
        while (position < this.gapStart) {
            this.gapEnd -= 1;
            this.gapStart -= 1;
            this.buffer[this.gapEnd] = this.buffer[this.gapStart];
            this.buffer[this.gapStart] = null;
        }
    }

    movePosition(position) {
        if (this.gapSize === 0) {
            // Bug fix, stop it moving on an empty gap
            this.grow(5, this.gapStart);
        }
        if (position < this.gapStart) {
            this.left(position);
        } else {
            this.right(position);
        }
    }

    insert(position, input) {
        if (position !== this.gapStart) {
            this.movePosition(position);
        }
        for (const char of input) {
            if (this.gapStart >= this.gapEnd) {
                this.grow(5, this.gapStart);
            }
            this.buffer[this.gapStart] = char;
            this.gapStart += 1;
            this.gapSize -= 1;
            this.gapEnd = this.gapStart + this.gapSize;
        }
    }

    delete(position) {
        if (position !== this.gapStart) {
            this.movePosition(position);
        }
        if (this.gapStart === 0) {
            return null; // never delete before the start of the buffer
        }
        this.gapStart -= 1;
        const deleted = this.buffer[this.gapStart];
        this.buffer[this.gapStart] = null;
        this.gapSize += 1;
        this.gapEnd = this.gapStart + this.gapSize;
        return deleted;
    }


    textContent() {
        return this.buffer.slice(0, this.gapStart)
            .concat(this.buffer.slice(this.gapEnd))
            .join("");
    }

    // Number of real characters, for cursor
    length() {
        return this.buffer.length - (this.gapEnd - this.gapStart);
    }

    // Python: __repr__ — debug printout showing the gap
    toString() {
        const before = this.buffer.slice(0, this.gapStart).join("");
        const gap = "_".repeat(this.gapEnd - this.gapStart);
        const after = this.buffer.slice(this.gapEnd).join("");
        return `${before}|${gap}|${after}`;
    }
}
